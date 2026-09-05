"""Migration recommendation and approval models."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import ApprovalDecision, ModernizationStrategy, RecommendationStatus
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.application import Application


class MigrationRecommendation(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """AI/deterministic recommendation for an application's modernization path."""

    __tablename__ = "migration_recommendations"

    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    external_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    strategy: Mapped[ModernizationStrategy] = mapped_column(
        Enum(
            ModernizationStrategy,
            name="modernization_strategy_enum",
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
    )
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    reasoning: Mapped[str] = mapped_column(Text, nullable=False)
    assumptions: Mapped[str | None] = mapped_column(Text, nullable=True)
    risks_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    alternatives: Mapped[list[str] | None] = mapped_column(ARRAY(String(64)), nullable=True)
    evidence_ids: Mapped[list[str] | None] = mapped_column(ARRAY(String(64)), nullable=True)
    status: Mapped[RecommendationStatus] = mapped_column(
        Enum(
            RecommendationStatus,
            name="recommendation_status_enum",
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
        default=RecommendationStatus.DRAFT,
    )
    details_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    application: Mapped[Application] = relationship(back_populates="recommendations")
    approvals: Mapped[list[Approval]] = relationship(back_populates="recommendation")


class Approval(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Human approval decision for a recommendation."""

    __tablename__ = "approvals"

    recommendation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("migration_recommendations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    decision: Mapped[ApprovalDecision] = mapped_column(
        Enum(
            ApprovalDecision,
            name="approval_decision_enum",
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
    )
    decided_by: Mapped[str] = mapped_column(String(255), nullable=False)
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    original_strategy: Mapped[str | None] = mapped_column(String(64), nullable=True)
    modified_strategy: Mapped[str | None] = mapped_column(String(64), nullable=True)
    evidence_ids: Mapped[list[str] | None] = mapped_column(ARRAY(String(64)), nullable=True)

    recommendation: Mapped[MigrationRecommendation] = relationship(back_populates="approvals")
