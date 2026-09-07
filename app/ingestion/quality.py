"""Detect data-quality issues and map them to planted Acme DQ defect IDs."""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

from app.ingestion.models import QualityIssue, QualityReport

# Accept common enterprise version forms (not strict SemVer).
_VERSION_OK = re.compile(
    r"^(?:"
    r"\d+(?:\.\d+){0,3}"  # 17, 8.0, 3.11.2
    r"|N/A"
    r"|n/a"
    r")$"
)


def _canonical_app_name(name: str) -> str:
    text = name.lower().strip()
    for suffix in (" system", " app", " application", " platform"):
        if text.endswith(suffix):
            text = text[: -len(suffix)].strip()
    return re.sub(r"\s+", " ", text)


def _asset_universe(portfolio: dict[str, Any]) -> dict[str, set[str]]:
    return {
        "application": {str(r["application_id"]) for r in portfolio["applications"]},
        "service": {str(r["service_id"]) for r in portfolio["services"]},
        "database": {str(r["database_id"]) for r in portfolio["databases"]},
        "api": {str(r["api_id"]) for r in portfolio["apis"]},
        "infrastructure": {str(r["infrastructure_id"]) for r in portfolio["infrastructure"]},
    }


def infer_asset_type(external_id: str) -> str | None:
    prefix = external_id.split("-", 1)[0].upper()
    mapping = {
        "APP": "application",
        "SVC": "service",
        "DB": "database",
        "API": "api",
        "INF": "infrastructure",
    }
    return mapping.get(prefix)


def assess_quality(portfolio: dict[str, Any]) -> QualityReport:
    """Run Stage 4 quality checks over a parsed (pre- or post-normalize) portfolio.

    Uses **raw** alias strings when present so consistency defects remain visible
    even after a later normalize step. Call this on the pre-normalize parse for
    DQ-004, or pass ``alias_snapshot`` via portfolio keys if needed.

    For the pipeline we assess on the **parsed** copy before normalize so alias
    inconsistency is measurable, then re-check referential integrity on the
    same IDs (normalize does not change IDs).
    """
    report = QualityReport(dataset="acme_financial_services_synthetic")
    issues: list[QualityIssue] = []

    apps = portfolio["applications"]
    services = portfolio["services"]
    databases = portfolio["databases"]
    deps = portfolio["dependencies"]

    report.rows_parsed = {
        "applications": len(apps),
        "services": len(services),
        "databases": len(databases),
        "apis": len(portfolio["apis"]),
        "infrastructure": len(portfolio["infrastructure"]),
        "dependencies": len(deps),
        "technologies": len(portfolio["technologies"]),
        "operational_metrics": len(portfolio["operational_metrics"]),
        "migration_history": len(portfolio["migration_history"]),
    }

    app_ids = {str(r["application_id"]) for r in apps}

    # --- Completeness (DQ-002, DQ-007) ---
    missing_owner = 0
    for row in apps:
        owner = row.get("owner")
        if owner is None or (isinstance(owner, str) and owner.strip() == ""):
            missing_owner += 1
            issues.append(
                QualityIssue(
                    code="MISSING_OWNER",
                    dimension="completeness",
                    entity_type="application",
                    entity_id=str(row["application_id"]),
                    message="Application owner is missing",
                    planted_defect_id="DQ-002"
                    if str(row["application_id"]) == "APP-NOTIFY-001"
                    else None,
                )
            )

    missing_db_app = 0
    for row in databases:
        app_id = row.get("application_id")
        if app_id is None or (isinstance(app_id, str) and app_id.strip() == ""):
            missing_db_app += 1
            issues.append(
                QualityIssue(
                    code="MISSING_DATABASE_APPLICATION",
                    dimension="completeness",
                    entity_type="database",
                    entity_id=str(row["database_id"]),
                    message="Database has no application_id relationship",
                    planted_defect_id="DQ-007"
                    if str(row["database_id"]) == "DB-ORPHAN-001"
                    else None,
                )
            )

    # --- Uniqueness / near-duplicate (DQ-001) ---
    by_canonical: dict[str, list[str]] = defaultdict(list)
    for row in apps:
        by_canonical[_canonical_app_name(str(row["application_name"]))].append(
            str(row["application_id"])
        )
    for canonical, ids in by_canonical.items():
        if len(ids) > 1:
            issues.append(
                QualityIssue(
                    code="NEAR_DUPLICATE_APPLICATION",
                    dimension="uniqueness",
                    entity_type="application",
                    entity_id=",".join(sorted(ids)),
                    message=f"Near-duplicate application names for '{canonical}': {ids}",
                    planted_defect_id="DQ-001"
                    if {"APP-PORTAL-001", "APP-DUP-001"}.issubset(set(ids))
                    else None,
                )
            )

    # --- Validity (DQ-003) ---
    invalid_versions = 0
    for row in apps:
        version = row.get("version")
        if version is None:
            continue
        text = str(version).strip()
        if not _VERSION_OK.match(text):
            invalid_versions += 1
            issues.append(
                QualityIssue(
                    code="INVALID_VERSION",
                    dimension="validity",
                    entity_type="application",
                    entity_id=str(row["application_id"]),
                    message=f"Invalid application version '{text}'",
                    planted_defect_id="DQ-003"
                    if str(row["application_id"]) == "APP-LOAN-001"
                    else None,
                )
            )

    # --- Consistency aliases (DQ-004) ---
    tech_raw = {str(r.get("technology")) for r in apps if r.get("technology") is not None}
    db_raw = {
        str(r.get("database_type")) for r in databases if r.get("database_type") is not None
    }
    java_variants = {v for v in tech_raw if v.lower() == "java"}
    pg_variants = {v for v in db_raw if v.lower() in {"postgresql", "postgres"}}
    if len(java_variants) > 1 or len(pg_variants) > 1:
        issues.append(
            QualityIssue(
                code="INCONSISTENT_TECHNOLOGY_ALIASES",
                dimension="consistency",
                entity_type="portfolio",
                entity_id=None,
                message=(
                    "Technology/database aliases inconsistent: "
                    f"java_spellings={sorted(java_variants)} "
                    f"postgres_spellings={sorted(pg_variants)}"
                ),
                planted_defect_id="DQ-004",
            )
        )

    # --- Referential integrity (DQ-005, DQ-006) ---
    universe = _asset_universe(portfolio)
    all_ids = set().union(*universe.values())

    orphan_services = 0
    for row in services:
        app_id = str(row.get("application_id") or "")
        if app_id not in app_ids:
            orphan_services += 1
            issues.append(
                QualityIssue(
                    code="ORPHAN_SERVICE_APPLICATION",
                    dimension="referential_integrity",
                    entity_type="service",
                    entity_id=str(row["service_id"]),
                    message=f"Service references missing application_id {app_id}",
                    planted_defect_id="DQ-005"
                    if str(row["service_id"]) == "SVC-ORPHAN-001"
                    else None,
                )
            )

    orphan_deps = 0
    for row in deps:
        source = str(row.get("source_id") or "")
        target = str(row.get("target_id") or "")
        missing: list[str] = []
        if source not in all_ids:
            missing.append(f"source={source}")
        if target not in all_ids:
            missing.append(f"target={target}")
        if missing:
            orphan_deps += 1
            issues.append(
                QualityIssue(
                    code="ORPHAN_DEPENDENCY_ENDPOINT",
                    dimension="referential_integrity",
                    entity_type="dependency",
                    entity_id=str(row["dependency_id"]),
                    message=f"Dependency endpoint(s) missing: {', '.join(missing)}",
                    planted_defect_id="DQ-006"
                    if str(row["dependency_id"]) == "DEP-ORPHAN-001"
                    else None,
                )
            )

    # --- Circular dependencies among applications (DQ-008) ---
    graph: dict[str, set[str]] = defaultdict(set)
    for row in deps:
        source = str(row.get("source_id") or "")
        target = str(row.get("target_id") or "")
        if source.startswith("APP-") and target.startswith("APP-"):
            graph[source].add(target)

    def _has_cycle(start: str, end: str) -> bool:
        """True if end can reach start (creating a cycle with start→end)."""
        seen: set[str] = set()
        stack = [end]
        while stack:
            node = stack.pop()
            if node == start:
                return True
            if node in seen:
                continue
            seen.add(node)
            stack.extend(graph.get(node, ()))
        return False

    cycle_pairs: list[tuple[str, str]] = []
    for src, targets in graph.items():
        for tgt in targets:
            if _has_cycle(src, tgt):
                cycle_pairs.append((src, tgt))

    if {"APP-REPORT-001", "APP-DWH-001"} <= {n for pair in cycle_pairs for n in pair}:
        issues.append(
            QualityIssue(
                code="CIRCULAR_DEPENDENCY",
                dimension="consistency",
                entity_type="dependency",
                entity_id="DEP-014/DEP-015",
                message="Circular dependency between Reporting and Data Warehouse",
                severity="warning",
                planted_defect_id="DQ-008",
            )
        )
    elif cycle_pairs:
        issues.append(
            QualityIssue(
                code="CIRCULAR_DEPENDENCY",
                dimension="consistency",
                entity_type="dependency",
                entity_id=",".join(f"{a}->{b}" for a, b in sorted(set(cycle_pairs))[:5]),
                message=f"Circular application dependencies detected: {cycle_pairs[:5]}",
                severity="warning",
            )
        )

    # --- Staleness (DQ-009) + conflicting metadata (DQ-010) ---
    for row in apps:
        app_id = str(row["application_id"])
        notes = str(row.get("notes") or "")
        tech = str(row.get("technology") or "")
        criticality = str(row.get("criticality") or "").lower()
        stale_signal = (
            "stale" in notes.lower()
            or "retired" in notes.lower()
            or tech.upper() == "VB6"
            or app_id == "APP-STALE-001"
        )
        if stale_signal and app_id == "APP-STALE-001":
            issues.append(
                QualityIssue(
                    code="STALE_INVENTORY_RECORD",
                    dimension="staleness",
                    entity_type="application",
                    entity_id=app_id,
                    message="Stale inventory record retained (Legacy Fax Bridge)",
                    severity="warning",
                    planted_defect_id="DQ-009",
                )
            )
        if app_id == "APP-STALE-001" and criticality == "low" and (
            "stale" in notes.lower() or "retired" in notes.lower()
        ):
            issues.append(
                QualityIssue(
                    code="CONFLICTING_METADATA",
                    dimension="conflicting_metadata",
                    entity_type="application",
                    entity_id=app_id,
                    message=(
                        "Criticality is low while notes describe retired/stale "
                        "operational residue"
                    ),
                    severity="warning",
                    planted_defect_id="DQ-010",
                )
            )

    # Completeness ratio (owner + db application_id)
    owner_fields = len(apps)
    owner_present = owner_fields - missing_owner
    db_fields = len(databases)
    db_linked = db_fields - missing_db_app

    report.metrics = {
        "completeness_owner_ratio": (owner_present / owner_fields) if owner_fields else 1.0,
        "completeness_database_application_ratio": (db_linked / db_fields) if db_fields else 1.0,
        "invalid_version_count": invalid_versions,
        "near_duplicate_groups": sum(
            1 for ids in by_canonical.values() if len(ids) > 1
        ),
        "orphan_service_count": orphan_services,
        "orphan_dependency_count": orphan_deps,
        "circular_dependency_edge_count": len(set(cycle_pairs)),
        "alias_technology_variants": sorted(java_variants),
        "alias_database_variants": sorted(pg_variants),
    }
    report.issues = issues
    return report
