"""Unit tests for Stage 4 data engineering pipeline (no DB required)."""

from __future__ import annotations

from pathlib import Path

from app.ingestion.dedupe import dedupe_applications
from app.ingestion.normalize import normalize_database_type, normalize_technology
from app.ingestion.parse import parse_acme_raw
from app.ingestion.pipeline import run_acme_pipeline
from app.ingestion.quality import assess_quality, infer_asset_type


def test_parse_acme_raw_counts() -> None:
    raw = parse_acme_raw()
    assert raw["project"]["external_id"] == "PROJ-ACME-001"
    assert len(raw["applications"]) >= 10
    assert len(raw["services"]) >= 10
    assert len(raw["dependencies"]) >= 15
    assert len(raw["technologies"]) >= 5


def test_normalize_aliases() -> None:
    assert normalize_technology("java") == "Java"
    assert normalize_technology("Java") == "Java"
    assert normalize_database_type("postgres") == "PostgreSQL"
    assert normalize_database_type("Postgres") == "PostgreSQL"
    assert normalize_database_type("PostgreSQL") == "PostgreSQL"


def test_infer_asset_type() -> None:
    assert infer_asset_type("APP-PAY-001") == "application"
    assert infer_asset_type("DB-PAY-001") == "database"
    assert infer_asset_type("INF-MQ-001") == "infrastructure"
    assert infer_asset_type("UNKNOWN") is None


def test_quality_detects_planted_defects_dq001_to_dq010() -> None:
    report = assess_quality(parse_acme_raw())
    detected = set(report.planted_defect_ids_detected)
    expected = {f"DQ-{i:03d}" for i in range(1, 11)}
    assert expected.issubset(detected), f"missing {expected - detected}; got {detected}"


def test_quality_metrics_populated() -> None:
    report = assess_quality(parse_acme_raw())
    assert report.metrics["orphan_service_count"] >= 1
    assert report.metrics["orphan_dependency_count"] >= 1
    assert report.metrics["invalid_version_count"] >= 1
    assert report.metrics["completeness_owner_ratio"] < 1.0


def test_dedupe_rejects_portal_duplicate() -> None:
    apps = parse_acme_raw()["applications"]
    kept, rejected, _issues = dedupe_applications(apps)
    kept_ids = {str(r["application_id"]) for r in kept}
    assert "APP-PORTAL-001" in kept_ids
    assert "APP-DUP-001" in rejected
    assert "APP-DUP-001" not in kept_ids


def test_pipeline_dry_run_writes_report(tmp_path: Path) -> None:
    report_file = tmp_path / "quality_report.json"
    result = run_acme_pipeline(
        session=None,
        persist=False,
        write_report=True,
        report_path=report_file,
    )
    assert result.stored is False
    assert report_file.is_file()
    assert "DQ-005" in result.quality_report.planted_defect_ids_detected
    # Clean inventory excludes orphan service / dup app
    assert result.quality_report.rows_rejected["applications"] >= 1
    assert result.quality_report.rows_rejected["services"] >= 1
    assert result.quality_report.rows_rejected["dependencies"] >= 1
