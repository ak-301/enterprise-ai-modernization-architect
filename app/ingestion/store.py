"""Persist validated Acme inventory into PostgreSQL."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    ApiAsset,
    Application,
    Criticality,
    DatabaseAsset,
    Dependency,
    DeploymentModel,
    EnvironmentName,
    InfrastructureResource,
    Project,
    Service,
    Technology,
)


def _parse_date(value: Any) -> date | None:
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    text = str(value).strip()
    if not text or text.lower() == "null":
        return None
    return date.fromisoformat(text[:10])


def _criticality(value: Any) -> Criticality:
    try:
        return Criticality(str(value).strip().lower())
    except ValueError:
        return Criticality.MEDIUM


def _environment(value: Any) -> EnvironmentName:
    try:
        return EnvironmentName(str(value).strip().lower())
    except ValueError:
        return EnvironmentName.PRODUCTION


def _deployment(value: Any) -> DeploymentModel:
    try:
        return DeploymentModel(str(value).strip().lower())
    except ValueError:
        return DeploymentModel.ON_PREM


def store_portfolio(session: Session, portfolio: dict[str, Any]) -> dict[str, int]:
    """Replace any existing Acme project and insert the clean portfolio.

    Operational metrics and migration history are not persisted in Stage 4
    (no ORM tables yet); they remain available from raw files for later stages.
    """
    meta = portfolio["project"]
    external_id = str(meta["external_id"])

    existing = session.scalar(select(Project).where(Project.external_id == external_id))
    if existing is not None:
        session.delete(existing)
        session.flush()

    # Technologies are global catalog rows — upsert by external_id.
    for tech in portfolio["technologies"]:
        tech_id = str(tech["external_id"])
        row = session.scalar(select(Technology).where(Technology.external_id == tech_id))
        if row is None:
            row = Technology(external_id=tech_id)
            session.add(row)
        row.name = str(tech["name"])
        row.category = str(tech["category"])
        row.vendor = tech.get("vendor")
        row.lifecycle_status = str(tech.get("lifecycle_status") or "supported")
        row.end_of_support = _parse_date(tech.get("end_of_support"))
        row.notes = tech.get("notes")

    project = Project(
        external_id=external_id,
        name=str(meta["name"]),
        organization_name=str(meta["organization_name"]),
        description=meta.get("description"),
        industry=meta.get("industry"),
    )
    session.add(project)
    session.flush()

    app_uuid: dict[str, UUID] = {}
    for row in portfolio["applications"]:
        app = Application(
            project_id=project.id,
            external_id=str(row["application_id"]),
            name=str(row["application_name"]),
            owner=row.get("owner"),
            business_unit=row.get("business_unit"),
            technology=row.get("technology"),
            version=None
            if str(row.get("version") or "") == "not-a-semver"
            else row.get("version"),
            criticality=_criticality(row.get("criticality")),
            environment=_environment(row.get("environment")),
            deployment_model=_deployment(row.get("deployment_model")),
            age_years=float(row["age_years"]) if row.get("age_years") is not None else None,
            description=row.get("notes"),
            is_active=bool(row.get("is_active", True)),
        )
        session.add(app)
        session.flush()
        app_uuid[app.external_id] = app.id

    for row in portfolio["services"]:
        session.add(
            Service(
                application_id=app_uuid[str(row["application_id"])],
                external_id=str(row["service_id"]),
                name=str(row["service_name"]),
                language=row.get("language"),
                framework=row.get("framework"),
                version=row.get("version"),
                replicas=int(row["replicas"]) if row.get("replicas") is not None else None,
                deployment_environment=_environment(row.get("deployment_environment")),
            )
        )

    for row in portfolio["databases"]:
        app_ext = row.get("application_id")
        session.add(
            DatabaseAsset(
                application_id=app_uuid.get(str(app_ext)) if app_ext else None,
                external_id=str(row["database_id"]),
                name=str(row["database_name"]),
                database_type=str(row["database_type"]),
                version=row.get("version"),
                size_gb=float(row["size_gb"]) if row.get("size_gb") is not None else None,
                table_count=int(row["table_count"])
                if row.get("table_count") is not None
                else None,
                daily_growth_gb=float(row["daily_growth_gb"])
                if row.get("daily_growth_gb") is not None
                else None,
                criticality=_criticality(row.get("criticality")),
                contains_sensitive_data=bool(row.get("contains_sensitive_data")),
            )
        )

    for row in portfolio["apis"]:
        session.add(
            ApiAsset(
                application_id=app_uuid[str(row["application_id"])],
                external_id=str(row["api_id"]),
                name=str(row["api_name"]),
                protocol=str(row.get("protocol") or "REST"),
                base_path=row.get("base_path"),
                auth_method=row.get("auth_method"),
                average_latency_ms=int(row["average_latency_ms"])
                if row.get("average_latency_ms") is not None
                else None,
            )
        )

    for row in portfolio["infrastructure"]:
        session.add(
            InfrastructureResource(
                project_id=project.id,
                external_id=str(row["infrastructure_id"]),
                name=str(row["name"]),
                resource_type=str(row["resource_type"]),
                provider=row.get("provider"),
                region=row.get("region"),
                technology=row.get("technology"),
            )
        )

    for row in portfolio["dependencies"]:
        session.add(
            Dependency(
                project_id=project.id,
                external_id=str(row["dependency_id"]),
                source_asset_type=row["source_asset_type"],
                source_external_id=str(row["source_id"]),
                target_asset_type=row["target_asset_type"],
                target_external_id=str(row["target_id"]),
                dependency_type=row["dependency_type_enum"],
                latency_ms=int(row["latency_ms"]) if row.get("latency_ms") is not None else None,
                traffic_per_day=float(row["traffic_per_day"])
                if row.get("traffic_per_day") is not None
                else None,
                criticality=_criticality(row.get("criticality")),
            )
        )

    session.flush()
    return {
        "projects": 1,
        "applications": len(portfolio["applications"]),
        "services": len(portfolio["services"]),
        "databases": len(portfolio["databases"]),
        "apis": len(portfolio["apis"]),
        "infrastructure": len(portfolio["infrastructure"]),
        "dependencies": len(portfolio["dependencies"]),
        "technologies": len(portfolio["technologies"]),
    }
