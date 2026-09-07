"""CLI: python -m app.ingestion [--no-persist] [--no-report]."""

from __future__ import annotations

import argparse
import json
import sys

from app.database.session import SessionLocal
from app.ingestion.pipeline import pipeline_summary, run_acme_pipeline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the Acme synthetic data engineering pipeline (Stage 4)."
    )
    parser.add_argument(
        "--no-persist",
        action="store_true",
        help="Assess and report only; do not write to PostgreSQL.",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip writing data/processed/acme/quality_report.json.",
    )
    args = parser.parse_args(argv)

    persist = not args.no_persist
    session = SessionLocal() if persist else None
    try:
        result = run_acme_pipeline(
            session,
            persist=persist,
            write_report=not args.no_report,
        )
        if persist and session is not None:
            session.commit()
        print(json.dumps(pipeline_summary(result), indent=2))
        return 0
    except Exception as exc:
        if session is not None:
            session.rollback()
        print(f"ingestion failed: {exc}", file=sys.stderr)
        return 1
    finally:
        if session is not None:
            session.close()


if __name__ == "__main__":
    raise SystemExit(main())
