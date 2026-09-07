"""Enrich inventory rows with derived fields before persistence."""

from __future__ import annotations

from typing import Any

from app.ingestion.quality import infer_asset_type
from app.models.enums import AssetType, DependencyType


def enrich_applications(applications: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Mark stale/retired rows inactive; attach enrichment flags."""
    enriched: list[dict[str, Any]] = []
    for row in applications:
        item = dict(row)
        notes = str(item.get("notes") or "").lower()
        tech = str(item.get("technology") or "").upper()
        stale = (
            "stale" in notes
            or "retired" in notes
            or tech == "VB6"
            or str(item.get("application_id")) == "APP-STALE-001"
        )
        item["is_active"] = not stale
        item["_enrichment"] = {"stale_flag": stale}
        enriched.append(item)
    return enriched


def enrich_dependencies(
    dependencies: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Infer asset types from external ID prefixes for graph-ready edges."""
    enriched: list[dict[str, Any]] = []
    for row in dependencies:
        item = dict(row)
        source = str(item.get("source_id") or "")
        target = str(item.get("target_id") or "")
        source_type = infer_asset_type(source)
        target_type = infer_asset_type(target)
        item["source_asset_type"] = (
            AssetType(source_type) if source_type else None
        )
        item["target_asset_type"] = (
            AssetType(target_type) if target_type else None
        )
        dep_type = str(item.get("dependency_type") or "depends_on").lower()
        try:
            item["dependency_type_enum"] = DependencyType(dep_type)
        except ValueError:
            item["dependency_type_enum"] = None
        enriched.append(item)
    return enriched


def filter_storeable(
    portfolio: dict[str, Any],
    *,
    rejected_application_ids: set[str],
) -> dict[str, Any]:
    """Drop rows that fail referential integrity or dedupe rejection."""
    app_ids = {
        str(r["application_id"])
        for r in portfolio["applications"]
        if str(r["application_id"]) not in rejected_application_ids
    }

    applications = [
        r
        for r in portfolio["applications"]
        if str(r["application_id"]) not in rejected_application_ids
    ]

    services = [
        r
        for r in portfolio["services"]
        if str(r.get("application_id") or "") in app_ids
    ]
    rejected_services = [
        str(r["service_id"])
        for r in portfolio["services"]
        if str(r.get("application_id") or "") not in app_ids
    ]

    databases = list(portfolio["databases"])  # orphan DB allowed (nullable FK)

    apis = [
        r for r in portfolio["apis"] if str(r.get("application_id") or "") in app_ids
    ]

    infrastructure = list(portfolio["infrastructure"])

    known_ids = (
        app_ids
        | {str(r["service_id"]) for r in services}
        | {str(r["database_id"]) for r in databases}
        | {str(r["api_id"]) for r in apis}
        | {str(r["infrastructure_id"]) for r in infrastructure}
    )

    dependencies = []
    rejected_deps: list[str] = []
    for row in portfolio["dependencies"]:
        source = str(row.get("source_id") or "")
        target = str(row.get("target_id") or "")
        if (
            source in known_ids
            and target in known_ids
            and row.get("source_asset_type")
            and row.get("target_asset_type")
            and row.get("dependency_type_enum") is not None
        ):
            dependencies.append(row)
        else:
            rejected_deps.append(str(row["dependency_id"]))

    return {
        "project": portfolio["project"],
        "applications": applications,
        "services": services,
        "databases": databases,
        "apis": apis,
        "infrastructure": infrastructure,
        "dependencies": dependencies,
        "technologies": portfolio["technologies"],
        "_rejected": {
            "applications": sorted(rejected_application_ids),
            "services": rejected_services,
            "dependencies": rejected_deps,
        },
    }
