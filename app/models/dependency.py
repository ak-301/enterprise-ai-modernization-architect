"""Dependency edge model for the enterprise topology."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import AssetType, Criticality, DependencyType
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.project import Project


class Dependency(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Directed dependency between two portfolio assets.

    Assets are referenced by type + external business ID so the graph can
    span applications, services, databases, APIs, and infrastructure
    without a single polymorphic FK. Stage 4 validation enforces that
    referenced external IDs exist.
    """

    __tablename__ = "dependencies"
    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "external_id",
            name="uq_dependencies_project_external_id",
        ),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    external_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    source_asset_type: Mapped[AssetType] = mapped_column(
        Enum(AssetType, name="asset_type_enum", values_callable=lambda e: [x.value for x in e]),
        nullable=False,
    )
    source_external_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    target_asset_type: Mapped[AssetType] = mapped_column(
        Enum(
            AssetType,
            name="asset_type_enum",
            create_constraint=False,
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
    )
    target_external_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    dependency_type: Mapped[DependencyType] = mapped_column(
        Enum(
            DependencyType,
            name="dependency_type_enum",
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
    )
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    traffic_per_day: Mapped[float | None] = mapped_column(Float, nullable=True)
    criticality: Mapped[Criticality] = mapped_column(
        Enum(
            Criticality,
            name="criticality_enum",
            create_constraint=False,
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
        default=Criticality.MEDIUM,
    )

    project: Mapped[Project] = relationship(back_populates="dependencies")
