"""Risk assessment model."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import RiskCategory, RiskSeverity
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.application import Application


class Risk(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Assessed risk attached to an application (or portfolio-level later)."""

    __tablename__ = "risks"

    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    external_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    category: Mapped[RiskCategory] = mapped_column(
        Enum(
            RiskCategory,
            name="risk_category_enum",
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    severity: Mapped[RiskSeverity] = mapped_column(
        Enum(
            RiskSeverity,
            name="risk_severity_enum",
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
    )
    likelihood: Mapped[int] = mapped_column(Integer, nullable=False)
    impact: Mapped[int] = mapped_column(Integer, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    mitigation: Mapped[str | None] = mapped_column(Text, nullable=True)
    evidence_ids: Mapped[list[str] | None] = mapped_column(ARRAY(String(64)), nullable=True)

    application: Mapped[Application] = relationship(back_populates="risks")
