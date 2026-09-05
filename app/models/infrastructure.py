"""Infrastructure resource inventory model."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.project import Project


class InfrastructureResource(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Compute, queue, cache, network, or other infrastructure asset."""

    __tablename__ = "infrastructure_resources"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    external_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(128), nullable=False)
    provider: Mapped[str | None] = mapped_column(String(128), nullable=True)
    region: Mapped[str | None] = mapped_column(String(128), nullable=True)
    technology: Mapped[str | None] = mapped_column(String(255), nullable=True)

    project: Mapped[Project] = relationship(back_populates="infrastructure_resources")
