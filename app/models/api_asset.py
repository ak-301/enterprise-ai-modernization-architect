"""API inventory model."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.application import Application


class ApiAsset(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """API endpoint or API product exposed by an application."""

    __tablename__ = "api_assets"

    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    external_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    protocol: Mapped[str] = mapped_column(String(64), nullable=False, default="REST")
    base_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    auth_method: Mapped[str | None] = mapped_column(String(128), nullable=True)
    average_latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    application: Mapped[Application] = relationship(back_populates="apis")
