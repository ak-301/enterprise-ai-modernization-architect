"""Integration tests for Stage 2 ORM persistence against PostgreSQL."""

from __future__ import annotations

import pytest
from app.models import (
    Application,
    AssetType,
    Criticality,
    Dependency,
    DependencyType,
    EnvironmentName,
    Project,
    Service,
)
from app.schemas.inventory import ApplicationRead, ProjectRead
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def test_project_application_service_roundtrip(db_session: Session) -> None:
    project = Project(
        external_id="PROJ-TEST-STAGE2",
        name="Stage 2 Test Project",
        organization_name="Acme Financial Services",
        industry="financial_services",
    )
    db_session.add(project)
    db_session.flush()

    app = Application(
        project_id=project.id,
        external_id="APP-TEST-PAY",
        name="Payment Processing",
        owner="payments-team",
        technology="Java",
        criticality=Criticality.HIGH,
        environment=EnvironmentName.PRODUCTION,
    )
    db_session.add(app)
    db_session.flush()

    service = Service(
        application_id=app.id,
        external_id="SVC-TEST-PAY-API",
        name="payment-api",
        language="Java",
        framework="Spring Boot",
        replicas=3,
    )
    db_session.add(service)
    db_session.flush()

    loaded = db_session.scalar(select(Application).where(Application.external_id == "APP-TEST-PAY"))
    assert loaded is not None
    assert loaded.project.organization_name == "Acme Financial Services"
    assert len(loaded.services) == 1
    assert loaded.services[0].name == "payment-api"

    project_schema = ProjectRead.model_validate(project)
    app_schema = ApplicationRead.model_validate(loaded)
    assert project_schema.external_id == "PROJ-TEST-STAGE2"
    assert app_schema.name == "Payment Processing"


def test_dependency_persists(db_session: Session) -> None:
    project = Project(
        external_id="PROJ-TEST-DEP",
        name="Dep Test",
        organization_name="Acme Financial Services",
    )
    db_session.add(project)
    db_session.flush()

    dep = Dependency(
        project_id=project.id,
        external_id="DEP-TEST-001",
        source_asset_type=AssetType.APPLICATION,
        source_external_id="APP-PAY",
        target_asset_type=AssetType.APPLICATION,
        target_external_id="APP-IDP",
        dependency_type=DependencyType.CALLS,
        criticality=Criticality.CRITICAL,
    )
    db_session.add(dep)
    db_session.flush()

    loaded = db_session.scalar(select(Dependency).where(Dependency.external_id == "DEP-TEST-001"))
    assert loaded is not None
    assert loaded.target_external_id == "APP-IDP"


def test_duplicate_application_external_id_rejected(db_session: Session) -> None:
    project = Project(
        external_id="PROJ-TEST-DUP",
        name="Dup Test",
        organization_name="Acme Financial Services",
    )
    db_session.add(project)
    db_session.flush()

    db_session.add(
        Application(
            project_id=project.id,
            external_id="APP-DUP",
            name="One",
        )
    )
    db_session.flush()

    db_session.add(
        Application(
            project_id=project.id,
            external_id="APP-DUP",
            name="Two",
        )
    )
    with pytest.raises(IntegrityError):
        db_session.flush()
