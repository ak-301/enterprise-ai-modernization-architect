"""Cost estimate model."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.application import Application


class CostEstimate(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Transparent cost estimate with low/base/high bands.

    Assumptions are stored explicitly. Values are model estimates (ASSUMED),
    not measured Azure invoices.
    """

    __tablename__ = "cost_estimates"

    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    external_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="USD")
    one_time_low: Mapped[float] = mapped_column(Float, nullable=False)
    one_time_base: Mapped[float] = mapped_column(Float, nullable=False)
    one_time_high: Mapped[float] = mapped_column(Float, nullable=False)
    monthly_low: Mapped[float] = mapped_column(Float, nullable=False)
    monthly_base: Mapped[float] = mapped_column(Float, nullable=False)
    monthly_high: Mapped[float] = mapped_column(Float, nullable=False)
    assumptions: Mapped[str] = mapped_column(Text, nullable=False)
    breakdown_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)

    application: Mapped[Application] = relationship(back_populates="cost_estimates")
