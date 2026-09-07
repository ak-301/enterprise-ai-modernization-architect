"""Integration: Stage 4 load + Stage 5 graph from PostgreSQL."""

from __future__ import annotations

from app.graph.pipeline import analyze_project_graph
from app.ingestion.pipeline import run_acme_pipeline
from sqlalchemy.orm import Session


def test_graph_from_persisted_acme(db_session: Session) -> None:
    run_acme_pipeline(db_session, persist=True, write_report=False)
    analysis = analyze_project_graph(
        db_session,
        "PROJ-ACME-001",
        write_report=False,
    )
    assert analysis.node_count >= 20
    assert analysis.edge_count >= 15
    assert any(
        "APP-REPORT-001" in "|".join(cycle) and "APP-DWH-001" in "|".join(cycle)
        for cycle in analysis.cycles
    )
    idp = next(s for s in analysis.node_scores if s.external_id == "APP-IDP-001")
    assert idp.in_degree >= 3
