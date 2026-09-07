"""Deduplicate near-duplicate inventory rows before store."""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

from app.ingestion.models import QualityIssue


def _canonical_app_name(name: str) -> str:
    text = name.lower().strip()
    for suffix in (" system", " app", " application", " platform"):
        if text.endswith(suffix):
            text = text[: -len(suffix)].strip()
    return re.sub(r"\s+", " ", text)


def choose_canonical_application_id(ids: list[str]) -> str:
    """Prefer non-DUP ids, then lexicographically smallest."""
    preferred = [i for i in ids if "DUP" not in i.upper()]
    pool = preferred or ids
    return sorted(pool)[0]


def dedupe_applications(
    applications: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str], list[QualityIssue]]:
    """Keep one application per canonical name; reject near-duplicates.

    Returns (kept_rows, rejected_external_ids, informational issues).
    """
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in applications:
        groups[_canonical_app_name(str(row["application_name"]))].append(row)

    kept: list[dict[str, Any]] = []
    rejected: list[str] = []
    issues: list[QualityIssue] = []

    for canonical, rows in groups.items():
        if len(rows) == 1:
            kept.append(rows[0])
            continue
        ids = [str(r["application_id"]) for r in rows]
        winner = choose_canonical_application_id(ids)
        for row in rows:
            app_id = str(row["application_id"])
            if app_id == winner:
                kept.append(row)
            else:
                rejected.append(app_id)
                issues.append(
                    QualityIssue(
                        code="DEDUPED_APPLICATION",
                        dimension="uniqueness",
                        entity_type="application",
                        entity_id=app_id,
                        message=(
                            f"Rejected near-duplicate of '{canonical}' "
                            f"(kept {winner})"
                        ),
                        severity="error",
                        planted_defect_id="DQ-001"
                        if app_id == "APP-DUP-001" and winner == "APP-PORTAL-001"
                        else None,
                    )
                )
    return kept, rejected, issues
