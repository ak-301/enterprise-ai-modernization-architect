"""Evidence linkage model — ties claims to inventory or document sources."""

from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Evidence(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """A citeable evidence reference used by recommendations and risks.

    ``evidence_id`` is the public citation token (e.g. APP-017, DOC-MIG-008,
    DEP-204). Source rows are referenced loosely by type + external id so
    evidence can point at inventory or document chunks.
    """

    __tablename__ = "evidence"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    evidence_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(64), nullable=False)
    source_external_id: Mapped[str] = mapped_column(String(64), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
