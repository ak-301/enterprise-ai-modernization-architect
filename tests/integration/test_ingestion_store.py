"""Integration tests: Stage 4 Acme ingestion into PostgreSQL."""

from __future__ import annotations

from app.ingestion.pipeline import run_acme_pipeline
from app.models import Application, Dependency, Project, Service
from sqlalchemy import func, select
from sqlalchemy.orm import Session


def test_acme_pipeline_persists_clean_inventory(db_session: Session) -> None:
    result = run_acme_pipeline(
        db_session,
        persist=True,
        write_report=False,
    )
    assert result.stored is True
    detected = set(result.quality_report.planted_defect_ids_detected)
    assert {f"DQ-{i:03d}" for i in range(1, 11)}.issubset(detected)

    project = db_session.scalar(
        select(Project).where(Project.external_id == "PROJ-ACME-001")
    )
    assert project is not None
    assert project.organization_name == "Acme Financial Services"

    app_ids = set(
        db_session.scalars(
            select(Application.external_id).where(Application.project_id == project.id)
        ).all()
    )
    assert "APP-PORTAL-001" in app_ids
    assert "APP-DUP-001" not in app_ids
    assert "APP-STALE-001" in app_ids

    stale = db_session.scalar(
        select(Application).where(
            Application.project_id == project.id,
            Application.external_id == "APP-STALE-001",
        )
    )
    assert stale is not None
    assert stale.is_active is False

    loan = db_session.scalar(
        select(Application).where(
            Application.project_id == project.id,
            Application.external_id == "APP-LOAN-001",
        )
    )
    assert loan is not None
    assert loan.version is None  # invalid version stripped on store

    service_ids = set(
        db_session.scalars(
            select(Service.external_id).where(
                Service.application_id.in_(
                    select(Application.id).where(Application.project_id == project.id)
                )
            )
        ).all()
    )
    assert "SVC-ORPHAN-001" not in service_ids
    assert "SVC-PAY-API" in service_ids

    dep_ids = set(
        db_session.scalars(
            select(Dependency.external_id).where(Dependency.project_id == project.id)
        ).all()
    )
    assert "DEP-ORPHAN-001" not in dep_ids
    assert "DEP-001" in dep_ids

    app_count = db_session.scalar(
        select(func.count()).select_from(Application).where(
            Application.project_id == project.id
        )
    )
    assert app_count == result.quality_report.rows_stored["applications"]
