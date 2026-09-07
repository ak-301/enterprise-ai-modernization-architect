"""Deterministic graph metrics and bottleneck detection (Stage 5)."""

from __future__ import annotations

import networkx as nx

from app.graph.models import GraphAnalysis, GraphEdge, GraphNode, NodeScore


def _cycle_depth_map(graph: nx.DiGraph) -> dict[str, int | None]:
    """Longest-path depth from roots on a DAG condensation of the digraph.

    Nodes inside a strongly connected component share the component's depth.
    """
    if graph.number_of_nodes() == 0:
        return {}

    condensation = nx.condensation(graph)
    # Map condensation node -> members
    members: dict[int, list[str]] = {
        node: list(condensation.nodes[node]["members"]) for node in condensation.nodes
    }

    # Depth on condensation DAG (always acyclic)
    depths: dict[int, int] = {}
    for node in nx.topological_sort(condensation):
        preds = list(condensation.predecessors(node))
        if not preds:
            depths[node] = 0
        else:
            depths[node] = 1 + max(depths[p] for p in preds)

    result: dict[str, int | None] = {}
    for c_node, depth in depths.items():
        for member in members[c_node]:
            result[str(member)] = depth
    return result


def analyze_graph(
    graph: nx.DiGraph,
    nodes: list[GraphNode],
    edges: list[GraphEdge],
    *,
    project_external_id: str,
    bottleneck_top_n: int = 5,
) -> GraphAnalysis:
    """Compute degree, betweenness, depth, cycles, hubs, leaves, bottlenecks."""
    betweenness = (
        nx.betweenness_centrality(graph, normalized=True)
        if graph.number_of_nodes()
        else {}
    )
    depth_map = _cycle_depth_map(graph)

    scores: list[NodeScore] = []
    for node in nodes:
        key = node.key
        if key not in graph:
            continue
        scores.append(
            NodeScore(
                key=key,
                asset_type=node.asset_type,
                external_id=node.external_id,
                in_degree=int(graph.in_degree(key)),
                out_degree=int(graph.out_degree(key)),
                degree=int(graph.degree(key)),
                betweenness=float(betweenness.get(key, 0.0)),
                depth=depth_map.get(key),
            )
        )

    # Also score any edge endpoints not in the inventory node list
    known = {n.key for n in nodes}
    for key in graph.nodes:
        if key in known:
            continue
        asset_type, _, external_id = str(key).partition(":")
        scores.append(
            NodeScore(
                key=str(key),
                asset_type=asset_type or "unknown",
                external_id=external_id or str(key),
                in_degree=int(graph.in_degree(key)),
                out_degree=int(graph.out_degree(key)),
                degree=int(graph.degree(key)),
                betweenness=float(betweenness.get(key, 0.0)),
                depth=depth_map.get(str(key)),
            )
        )

    # Simple cycles among application nodes only (readable for interviews)
    app_subgraph = graph.subgraph(
        [n for n in graph.nodes if str(n).startswith("application:")]
    ).copy()
    cycles: list[list[str]] = []
    for cycle in nx.simple_cycles(app_subgraph):
        # Normalize rotation so reporting is stable
        rotated = cycle[cycle.index(min(cycle)) :] + cycle[: cycle.index(min(cycle))]
        cycles.append([str(x) for x in rotated])
    # Deduplicate identical cycles
    unique_cycles: list[list[str]] = []
    seen: set[tuple[str, ...]] = set()
    for cycle in cycles:
        key_t = tuple(cycle)
        if key_t not in seen:
            seen.add(key_t)
            unique_cycles.append(cycle)

    by_betweenness = sorted(scores, key=lambda s: s.betweenness, reverse=True)
    by_in_degree = sorted(scores, key=lambda s: s.in_degree, reverse=True)

    bottleneck_nodes = [s.key for s in by_betweenness[:bottleneck_top_n] if s.betweenness > 0]
    if len(bottleneck_nodes) < bottleneck_top_n:
        for s in by_in_degree:
            if s.key not in bottleneck_nodes and s.in_degree > 0:
                bottleneck_nodes.append(s.key)
            if len(bottleneck_nodes) >= bottleneck_top_n:
                break

    hubs = [s.key for s in by_in_degree[:bottleneck_top_n] if s.in_degree > 0]
    leaves = [
        s.key
        for s in scores
        if s.in_degree == 0 and s.out_degree > 0 and s.asset_type == "application"
    ]

    critical_edges = [
        e.external_id for e in edges if (e.criticality or "").lower() == "critical"
    ]

    return GraphAnalysis(
        project_external_id=project_external_id,
        node_count=graph.number_of_nodes(),
        edge_count=graph.number_of_edges(),
        nodes=list(nodes),
        edges=list(edges),
        node_scores=scores,
        cycles=unique_cycles,
        bottleneck_nodes=bottleneck_nodes,
        critical_edges=sorted(critical_edges),
        hubs_by_in_degree=hubs,
        leaf_nodes=sorted(leaves),
    )
