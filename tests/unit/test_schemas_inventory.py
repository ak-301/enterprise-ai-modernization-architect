"""Unit tests for Stage 2 Pydantic inventory schemas."""

from uuid import uuid4

import pytest
from app.models.enums import (
    AssetType,
    Criticality,
    DependencyType,
    DeploymentModel,
    EnvironmentName,
    ModernizationStrategy,
    RiskCategory,
    RiskSeverity,
)
from app.schemas.analysis import DependencyCreate, MigrationRecommendationCreate, RiskCreate
from app.schemas.inventory import ApplicationCreate, ProjectCreate
from pydantic import ValidationError


def test_project_create_valid() -> None:
    project = ProjectCreate(
        external_id="PROJ-ACME-001",
        name="Acme FY26 Modernization",
        organization_name="Acme Financial Services",
        industry="financial_services",
    )
    assert project.external_id == "PROJ-ACME-001"


def test_application_rejects_negative_age() -> None:
    with pytest.raises(ValidationError):
        ApplicationCreate(
            project_id=uuid4(),
            external_id="APP-001",
            name="Payment Processing",
            age_years=-1,
        )


def test_application_defaults() -> None:
    app = ApplicationCreate(
        project_id=uuid4(),
        external_id="APP-001",
        name="Payment Processing",
    )
    assert app.criticality == Criticality.MEDIUM
    assert app.environment == EnvironmentName.PRODUCTION
    assert app.deployment_model == DeploymentModel.ON_PREM


def test_dependency_create_valid() -> None:
    dep = DependencyCreate(
        project_id=uuid4(),
        external_id="DEP-001",
        source_asset_type=AssetType.APPLICATION,
        source_external_id="APP-PAY",
        target_asset_type=AssetType.APPLICATION,
        target_external_id="APP-IDP",
        dependency_type=DependencyType.CALLS,
    )
    assert dep.dependency_type == DependencyType.CALLS


def test_recommendation_confidence_bounds() -> None:
    with pytest.raises(ValidationError):
        MigrationRecommendationCreate(
            application_id=uuid4(),
            external_id="REC-001",
            strategy=ModernizationStrategy.REPLATFORM,
            confidence=1.5,
            reasoning="too confident",
        )


def test_risk_likelihood_bounds() -> None:
    with pytest.raises(ValidationError):
        RiskCreate(
            application_id=uuid4(),
            external_id="RISK-001",
            category=RiskCategory.TECHNICAL,
            title="Bad likelihood",
            severity=RiskSeverity.HIGH,
            likelihood=9,
            impact=3,
            score=27,
        )
