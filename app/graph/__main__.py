"""CLI: python -m app.graph [--from-db] [--no-report]."""

from __future__ import annotations

import argparse
import json
import sys

from app.database.session import SessionLocal
from app.graph.pipeline import analyze_acme_graph, analyze_project_graph, graph_summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Analyze Acme (or DB) dependency graph with NetworkX (Stage 5)."
    )
    parser.add_argument(
        "--from-db",
        action="store_true",
        help="Load project inventory from PostgreSQL instead of cleaned Acme files.",
    )
    parser.add_argument(
        "--project-id",
        default="PROJ-ACME-001",
        help="Project external_id when using --from-db (default: PROJ-ACME-001).",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip writing data/processed/acme/dependency_graph.json.",
    )
    args = parser.parse_args(argv)

    session = None
    try:
        if args.from_db:
            session = SessionLocal()
            analysis = analyze_project_graph(
                session,
                args.project_id,
                write_report=not args.no_report,
            )
        else:
            analysis = analyze_acme_graph(write_report=not args.no_report)
        print(json.dumps(graph_summary(analysis), indent=2))
        return 0
    except Exception as exc:
        print(f"graph analysis failed: {exc}", file=sys.stderr)
        return 1
    finally:
        if session is not None:
            session.close()


if __name__ == "__main__":
    raise SystemExit(main())
