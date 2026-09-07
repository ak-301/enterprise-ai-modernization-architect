"""Stage 5 orchestration: build graph → analyze → optional JSON export."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.graph.analysis import analyze_graph
from app.graph.builder import build_acme_graph, load_project_graph_from_db
from app.graph.models import GraphAnalysis
from app.synthetic.acme import REPO_ROOT

PROCESSED_DIR = REPO_ROOT / "data" / "processed" / "acme"
DEFAULT_GRAPH_REPORT_PATH = PROCESSED_DIR / "dependency_graph.json"


def write_graph_report(analysis: GraphAnalysis, path: Path = DEFAULT_GRAPH_REPORT_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(analysis.to_dict(), indent=2) + "\n", encoding="utf-8")
    return path


def analyze_acme_graph(
    *,
    write_report: bool = True,
    report_path: Path | None = None,
    bottleneck_top_n: int = 5,
) -> GraphAnalysis:
    """Analyze the cleaned synthetic Acme portfolio graph (no DB required)."""
    graph, nodes, edges, project_id = build_acme_graph()
    analysis = analyze_graph(
        graph,
        nodes,
        edges,
        project_external_id=project_id,
        bottleneck_top_n=bottleneck_top_n,
    )
    if write_report:
        write_graph_report(analysis, path=report_path or DEFAULT_GRAPH_REPORT_PATH)
    return analysis


def analyze_project_graph(
    session: Session,
    project_external_id: str,
    *,
    write_report: bool = False,
    report_path: Path | None = None,
    bottleneck_top_n: int = 5,
) -> GraphAnalysis:
    """Analyze a project already loaded in PostgreSQL."""
    graph, nodes, edges = load_project_graph_from_db(session, project_external_id)
    analysis = analyze_graph(
        graph,
        nodes,
        edges,
        project_external_id=project_external_id,
        bottleneck_top_n=bottleneck_top_n,
    )
    if write_report:
        write_graph_report(analysis, path=report_path or DEFAULT_GRAPH_REPORT_PATH)
    return analysis


def graph_summary(analysis: GraphAnalysis) -> dict[str, Any]:
    """Compact dict for CLI / tests."""
    top = sorted(analysis.node_scores, key=lambda s: s.betweenness, reverse=True)[:5]
    return {
        "project_external_id": analysis.project_external_id,
        "node_count": analysis.node_count,
        "edge_count": analysis.edge_count,
        "cycle_count": len(analysis.cycles),
        "cycles": analysis.cycles,
        "bottleneck_nodes": analysis.bottleneck_nodes,
        "hubs_by_in_degree": analysis.hubs_by_in_degree,
        "critical_edge_count": len(analysis.critical_edges),
        "top_betweenness": [
            {"key": s.key, "betweenness": s.betweenness, "in_degree": s.in_degree}
            for s in top
        ],
    }
