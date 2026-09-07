"""Unit tests for Stage 5 NetworkX dependency graph analysis."""

from __future__ import annotations

from pathlib import Path

from app.graph.analysis import analyze_graph
from app.graph.builder import build_acme_graph, build_digraph, node_key
from app.graph.models import GraphEdge, GraphNode
from app.graph.pipeline import analyze_acme_graph, graph_summary


def test_node_key_format() -> None:
    assert node_key("application", "APP-PAY-001") == "application:APP-PAY-001"


def test_build_acme_graph_has_core_nodes_and_edges() -> None:
    graph, nodes, edges, project_id = build_acme_graph()
    assert project_id == "PROJ-ACME-001"
    assert graph.number_of_nodes() >= 20
    assert graph.number_of_edges() >= 15
    assert any(n.external_id == "APP-IDP-001" for n in nodes)
    assert any(e.external_id == "DEP-001" for e in edges)
    # Orphan dependency rejected in Stage 4 clean portfolio
    assert all(e.external_id != "DEP-ORPHAN-001" for e in edges)


def test_analyze_acme_detects_reporting_dwh_cycle() -> None:
    analysis = analyze_acme_graph(write_report=False)
    assert analysis.edge_count >= 15
    flat = {"|".join(cycle) for cycle in analysis.cycles}
    assert any(
        "application:APP-REPORT-001" in c and "application:APP-DWH-001" in c for c in flat
    )


def test_idp_is_high_in_degree_hub() -> None:
    analysis = analyze_acme_graph(write_report=False)
    idp = next(s for s in analysis.node_scores if s.external_id == "APP-IDP-001")
    assert idp.in_degree >= 3
    assert "application:APP-IDP-001" in analysis.hubs_by_in_degree


def test_critical_edges_listed() -> None:
    analysis = analyze_acme_graph(write_report=False)
    assert "DEP-001" in analysis.critical_edges
    assert len(analysis.critical_edges) >= 3


def test_bottlenecks_non_empty() -> None:
    analysis = analyze_acme_graph(write_report=False)
    assert analysis.bottleneck_nodes
    summary = graph_summary(analysis)
    assert summary["node_count"] == analysis.node_count
    assert summary["cycle_count"] >= 1


def test_toy_graph_metrics() -> None:
    nodes = [
        GraphNode(key="application:A", asset_type="application", external_id="A"),
        GraphNode(key="application:B", asset_type="application", external_id="B"),
        GraphNode(key="application:C", asset_type="application", external_id="C"),
    ]
    edges = [
        GraphEdge(
            source_key="application:A",
            target_key="application:B",
            dependency_type="calls",
            external_id="E1",
            criticality="critical",
        ),
        GraphEdge(
            source_key="application:C",
            target_key="application:B",
            dependency_type="calls",
            external_id="E2",
            criticality="high",
        ),
    ]
    graph = build_digraph(nodes, edges)
    analysis = analyze_graph(graph, nodes, edges, project_external_id="TOY")
    b = next(s for s in analysis.node_scores if s.external_id == "B")
    assert b.in_degree == 2
    assert "E1" in analysis.critical_edges


def test_write_graph_report(tmp_path: Path) -> None:
    path = tmp_path / "dependency_graph.json"
    analysis = analyze_acme_graph(write_report=True, report_path=path)
    assert path.is_file()
    assert analysis.node_count > 0
