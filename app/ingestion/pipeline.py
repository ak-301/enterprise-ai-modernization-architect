"""Stage 4 orchestration: parse → quality → normalize → dedupe → enrich → store."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.ingestion.dedupe import dedupe_applications
from app.ingestion.enrich import enrich_applications, enrich_dependencies, filter_storeable
from app.ingestion.models import PipelineResult, QualityReport
from app.ingestion.normalize import normalize_portfolio
from app.ingestion.parse import parse_acme_raw
from app.ingestion.quality import assess_quality
from app.ingestion.store import store_portfolio
from app.synthetic.acme import REPO_ROOT

PROCESSED_DIR = REPO_ROOT / "data" / "processed" / "acme"
DEFAULT_REPORT_PATH = PROCESSED_DIR / "quality_report.json"


def write_quality_report(report: QualityReport, path: Path = DEFAULT_REPORT_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report.to_dict(), indent=2) + "\n", encoding="utf-8")
    return path


def run_acme_pipeline(
    session: Session | None = None,
    *,
    persist: bool = True,
    write_report: bool = True,
    report_path: Path | None = None,
) -> PipelineResult:
    """Execute the Acme data engineering pipeline.

    Parameters
    ----------
    session:
        SQLAlchemy session used when ``persist`` is True.
    persist:
        When True, store the clean inventory in PostgreSQL.
    write_report:
        When True, write ``quality_report.json`` under ``data/processed/acme/``.
    report_path:
        Optional override for the quality report path.
    """
    if persist and session is None:
        raise ValueError("session is required when persist=True")

    raw = parse_acme_raw()

    # Assess quality on raw parse so alias inconsistency (DQ-004) is visible.
    report = assess_quality(raw)

    normalized = normalize_portfolio(raw)
    kept_apps, rejected_app_ids, dedupe_issues = dedupe_applications(
        normalized["applications"]
    )
    # Prefer quality-report DQ-001 from assess_quality; keep dedupe actions as extra detail
    # only when assess_quality did not already plant DQ-001.
    if not any(i.planted_defect_id == "DQ-001" for i in report.issues):
        report.issues.extend(dedupe_issues)

    normalized["applications"] = enrich_applications(kept_apps)
    normalized["dependencies"] = enrich_dependencies(normalized["dependencies"])

    storeable = filter_storeable(
        normalized,
        rejected_application_ids=set(rejected_app_ids),
    )

    report.rows_rejected = {
        "applications": len(storeable["_rejected"]["applications"]),
        "services": len(storeable["_rejected"]["services"]),
        "dependencies": len(storeable["_rejected"]["dependencies"]),
    }

    stored_counts: dict[str, int] = {}
    if persist:
        assert session is not None
        stored_counts = store_portfolio(session, storeable)
        report.rows_stored = stored_counts
    else:
        report.rows_stored = {
            "applications": len(storeable["applications"]),
            "services": len(storeable["services"]),
            "databases": len(storeable["databases"]),
            "apis": len(storeable["apis"]),
            "infrastructure": len(storeable["infrastructure"]),
            "dependencies": len(storeable["dependencies"]),
            "technologies": len(storeable["technologies"]),
        }

    out_path: Path | None = None
    if write_report:
        out_path = write_quality_report(report, path=report_path or DEFAULT_REPORT_PATH)

    return PipelineResult(
        project_external_id=str(raw["project"]["external_id"]),
        quality_report=report,
        stored=persist,
        report_path=str(out_path) if out_path else None,
    )


def pipeline_summary(result: PipelineResult) -> dict[str, Any]:
    """Compact dict for CLI / tests."""
    qr = result.quality_report
    return {
        "project_external_id": result.project_external_id,
        "stored": result.stored,
        "report_path": result.report_path,
        "planted_defect_ids_detected": qr.planted_defect_ids_detected,
        "issue_count": len(qr.issues),
        "rows_stored": qr.rows_stored,
        "rows_rejected": qr.rows_rejected,
    }
