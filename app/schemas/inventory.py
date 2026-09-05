"""Pydantic schemas for projects and core inventory entities."""

from __future__ import annotations

from uuid import UUID

from pydantic import Field

from app.models.enums import Criticality, DeploymentModel, EnvironmentName
from app.schemas.common import ORMModel, TimestampSchema


class ProjectCreate(ORMModel):
    external_id: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=255)
    organization_name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    industry: str | None = Field(default=None, max_length=128)


class ProjectRead(ProjectCreate, TimestampSchema):
    id: UUID


class ApplicationCreate(ORMModel):
    project_id: UUID
    external_id: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=255)
    owner: str | None = Field(default=None, max_length=255)
    business_unit: str | None = Field(default=None, max_length=255)
    technology: str | None = Field(default=None, max_length=255)
    version: str | None = Field(default=None, max_length=64)
    criticality: Criticality = Criticality.MEDIUM
    environment: EnvironmentName = EnvironmentName.PRODUCTION
    deployment_model: DeploymentModel = DeploymentModel.ON_PREM
    age_years: float | None = Field(default=None, ge=0)
    description: str | None = None
    is_active: bool = True


class ApplicationRead(ApplicationCreate, TimestampSchema):
    id: UUID


class ServiceCreate(ORMModel):
    application_id: UUID
    external_id: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=255)
    language: str | None = None
    framework: str | None = None
    version: str | None = None
    replicas: int | None = Field(default=None, ge=0)
    deployment_environment: EnvironmentName = EnvironmentName.PRODUCTION


class ServiceRead(ServiceCreate, TimestampSchema):
    id: UUID


class DatabaseAssetCreate(ORMModel):
    application_id: UUID | None = None
    external_id: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=255)
    database_type: str = Field(min_length=1, max_length=128)
    version: str | None = None
    size_gb: float | None = Field(default=None, ge=0)
    table_count: int | None = Field(default=None, ge=0)
    daily_growth_gb: float | None = Field(default=None, ge=0)
    criticality: Criticality = Criticality.MEDIUM
    contains_sensitive_data: bool = False


class DatabaseAssetRead(DatabaseAssetCreate, TimestampSchema):
    id: UUID


class ApiAssetCreate(ORMModel):
    application_id: UUID
    external_id: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=255)
    protocol: str = Field(default="REST", max_length=64)
    base_path: str | None = None
    auth_method: str | None = None
    average_latency_ms: int | None = Field(default=None, ge=0)


class ApiAssetRead(ApiAssetCreate, TimestampSchema):
    id: UUID


class InfrastructureResourceCreate(ORMModel):
    project_id: UUID
    external_id: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=255)
    resource_type: str = Field(min_length=1, max_length=128)
    provider: str | None = None
    region: str | None = None
    technology: str | None = None


class InfrastructureResourceRead(InfrastructureResourceCreate, TimestampSchema):
    id: UUID
