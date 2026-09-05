"""Audit event model for governance trail."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import AuditAction
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.project import Project


class AuditEvent(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Append-only style audit record for significant system actions."""

    __tablename__ = "audit_events"

    project_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    action: Mapped[AuditAction] = mapped_column(
        Enum(AuditAction, name="audit_action_enum", values_callable=lambda e: [x.value for x in e]),
        nullable=False,
    )
    actor: Mapped[str] = mapped_column(String(255), nullable=False)
    entity_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    entity_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    request_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    details_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    project: Mapped[Project | None] = relationship(back_populates="audit_events")
