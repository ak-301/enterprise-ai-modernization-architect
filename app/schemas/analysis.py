"""Pydantic schemas for dependencies, documents, risks, recommendations."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import Field, field_validator

from app.models.enums import (
    ApprovalDecision,
    AssetType,
    AuditAction,
    Criticality,
    DependencyType,
    ModernizationStrategy,
    RecommendationStatus,
    RiskCategory,
    RiskSeverity,
)
from app.schemas.common import ORMModel, TimestampSchema


class DependencyCreate(ORMModel):
    project_id: UUID
    external_id: str = Field(min_length=1, max_length=64)
    source_asset_type: AssetType
    source_external_id: str = Field(min_length=1, max_length=64)
    target_asset_type: AssetType
    target_external_id: str = Field(min_length=1, max_length=64)
    dependency_type: DependencyType
    latency_ms: int | None = Field(default=None, ge=0)
    traffic_per_day: float | None = Field(default=None, ge=0)
    criticality: Criticality = Criticality.MEDIUM


class DependencyRead(DependencyCreate, TimestampSchema):
    id: UUID


class TechnologyCreate(ORMModel):
    external_id: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=255)
    category: str = Field(min_length=1, max_length=128)
    vendor: str | None = None
    lifecycle_status: str = Field(default="supported", max_length=64)
    end_of_support: date | None = None
    notes: str | None = None


class TechnologyRead(TechnologyCreate, TimestampSchema):
    id: UUID


class DocumentCreate(ORMModel):
    project_id: UUID
    external_id: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=512)
    doc_type: str = Field(min_length=1, max_length=128)
    source_path: str | None = None
    version: str | None = None


class DocumentRead(DocumentCreate, TimestampSchema):
    id: UUID


class DocumentChunkCreate(ORMModel):
    document_id: UUID
    evidence_id: str = Field(min_length=1, max_length=64)
    chunk_index: int = Field(ge=0)
    content: str = Field(min_length=1)
    token_count: int | None = Field(default=None, ge=0)
    metadata_json: dict | None = None


class DocumentChunkRead(DocumentChunkCreate, TimestampSchema):
    id: UUID


class EvidenceCreate(ORMModel):
    project_id: UUID
    evidence_id: str = Field(min_length=1, max_length=64)
    source_type: str = Field(min_length=1, max_length=64)
    source_external_id: str = Field(min_length=1, max_length=64)
    summary: str | None = None


class EvidenceRead(EvidenceCreate, TimestampSchema):
    id: UUID


class RiskCreate(ORMModel):
    application_id: UUID
    external_id: str = Field(min_length=1, max_length=64)
    category: RiskCategory
    title: str = Field(min_length=1, max_length=512)
    description: str | None = None
    severity: RiskSeverity
    likelihood: int = Field(ge=1, le=5)
    impact: int = Field(ge=1, le=5)
    score: float = Field(ge=0)
    mitigation: str | None = None
    evidence_ids: list[str] | None = None

    @field_validator("score")
    @classmethod
    def score_matches_likelihood_impact(cls, value: float, info: object) -> float:
        # Soft check only — engines may use weighted variants later.
        return value


class RiskRead(RiskCreate, TimestampSchema):
    id: UUID


class MigrationRecommendationCreate(ORMModel):
    application_id: UUID
    external_id: str = Field(min_length=1, max_length=64)
    strategy: ModernizationStrategy
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str = Field(min_length=1)
    assumptions: str | None = None
    risks_summary: str | None = None
    alternatives: list[str] | None = None
    evidence_ids: list[str] | None = None
    status: RecommendationStatus = RecommendationStatus.DRAFT
    details_json: dict | None = None


class MigrationRecommendationRead(MigrationRecommendationCreate, TimestampSchema):
    id: UUID


class ApprovalCreate(ORMModel):
    recommendation_id: UUID
    decision: ApprovalDecision
    decided_by: str = Field(min_length=1, max_length=255)
    decided_at: datetime
    reason: str | None = None
    original_strategy: str | None = None
    modified_strategy: str | None = None
    evidence_ids: list[str] | None = None


class ApprovalRead(ApprovalCreate, TimestampSchema):
    id: UUID


class MigrationWaveCreate(ORMModel):
    project_id: UUID
    external_id: str = Field(min_length=1, max_length=64)
    wave_number: int = Field(ge=0)
    name: str = Field(min_length=1, max_length=255)
    rationale: str | None = None


class MigrationWaveRead(MigrationWaveCreate, TimestampSchema):
    id: UUID


class MigrationWaveMembershipCreate(ORMModel):
    wave_id: UUID
    application_id: UUID
    rationale: str | None = None
    prerequisites: list[str] | None = None
    blockers: list[str] | None = None


class MigrationWaveMembershipRead(MigrationWaveMembershipCreate, TimestampSchema):
    id: UUID


class CostEstimateCreate(ORMModel):
    application_id: UUID
    external_id: str = Field(min_length=1, max_length=64)
    currency: str = Field(default="USD", min_length=3, max_length=8)
    one_time_low: float = Field(ge=0)
    one_time_base: float = Field(ge=0)
    one_time_high: float = Field(ge=0)
    monthly_low: float = Field(ge=0)
    monthly_base: float = Field(ge=0)
    monthly_high: float = Field(ge=0)
    assumptions: str = Field(min_length=1)
    breakdown_json: dict | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)


class CostEstimateRead(CostEstimateCreate, TimestampSchema):
    id: UUID


class AuditEventCreate(ORMModel):
    project_id: UUID | None = None
    action: AuditAction
    actor: str = Field(min_length=1, max_length=255)
    entity_type: str | None = None
    entity_id: str | None = None
    request_id: str | None = None
    message: str | None = None
    details_json: dict | None = None


class AuditEventRead(AuditEventCreate, TimestampSchema):
    id: UUID
