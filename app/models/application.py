"""Application inventory model."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, Float, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import Criticality, DeploymentModel, EnvironmentName
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.api_asset import ApiAsset
    from app.models.cost_estimate import CostEstimate
    from app.models.database_asset import DatabaseAsset
    from app.models.project import Project
    from app.models.recommendation import MigrationRecommendation
    from app.models.risk import Risk
    from app.models.service import Service


class Application(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Business application in the enterprise portfolio."""

    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("project_id", "external_id", name="uq_applications_project_external_id"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    external_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner: Mapped[str | None] = mapped_column(String(255), nullable=True)
    business_unit: Mapped[str | None] = mapped_column(String(255), nullable=True)
    technology: Mapped[str | None] = mapped_column(String(255), nullable=True)
    version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    criticality: Mapped[Criticality] = mapped_column(
        Enum(Criticality, name="criticality_enum", values_callable=lambda e: [x.value for x in e]),
        nullable=False,
        default=Criticality.MEDIUM,
    )
    environment: Mapped[EnvironmentName] = mapped_column(
        Enum(
            EnvironmentName,
            name="environment_name_enum",
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
        default=EnvironmentName.PRODUCTION,
    )
    deployment_model: Mapped[DeploymentModel] = mapped_column(
        Enum(
            DeploymentModel,
            name="deployment_model_enum",
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
        default=DeploymentModel.ON_PREM,
    )
    age_years: Mapped[float | None] = mapped_column(Float, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    project: Mapped[Project] = relationship(back_populates="applications")
    services: Mapped[list[Service]] = relationship(back_populates="application")
    databases: Mapped[list[DatabaseAsset]] = relationship(back_populates="application")
    apis: Mapped[list[ApiAsset]] = relationship(back_populates="application")
    risks: Mapped[list[Risk]] = relationship(back_populates="application")
    recommendations: Mapped[list[MigrationRecommendation]] = relationship(
        back_populates="application"
    )
    cost_estimates: Mapped[list[CostEstimate]] = relationship(back_populates="application")
