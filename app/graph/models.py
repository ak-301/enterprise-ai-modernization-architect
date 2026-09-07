"""Typed results for Stage 5 dependency graph analysis."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class GraphNode:
    key: str
    asset_type: str
    external_id: str
    name: str | None = None
    criticality: str | None = None


@dataclass(frozen=True)
class GraphEdge:
    source_key: str
    target_key: str
    dependency_type: str
    external_id: str
    criticality: str | None = None
    latency_ms: int | None = None
    traffic_per_day: float | None = None


@dataclass(frozen=True)
class NodeScore:
    key: str
    asset_type: str
    external_id: str
    in_degree: int
    out_degree: int
    degree: int
    betweenness: float
    depth: int | None


@dataclass
class GraphAnalysis:
    """Summary consumed by interviews, waves (Stage 10), and tests."""

    project_external_id: str
    node_count: int
    edge_count: int
    nodes: list[GraphNode] = field(default_factory=list)
    edges: list[GraphEdge] = field(default_factory=list)
    node_scores: list[NodeScore] = field(default_factory=list)
    cycles: list[list[str]] = field(default_factory=list)
    bottleneck_nodes: list[str] = field(default_factory=list)
    critical_edges: list[str] = field(default_factory=list)
    hubs_by_in_degree: list[str] = field(default_factory=list)
    leaf_nodes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_external_id": self.project_external_id,
            "node_count": self.node_count,
            "edge_count": self.edge_count,
            "cycles": self.cycles,
            "bottleneck_nodes": self.bottleneck_nodes,
            "critical_edges": self.critical_edges,
            "hubs_by_in_degree": self.hubs_by_in_degree,
            "leaf_nodes": self.leaf_nodes,
            "top_betweenness": [
                asdict(s)
                for s in sorted(self.node_scores, key=lambda n: n.betweenness, reverse=True)[:10]
            ],
            "nodes": [asdict(n) for n in self.nodes],
            "edges": [asdict(e) for e in self.edges],
            "node_scores": [asdict(s) for s in self.node_scores],
        }
