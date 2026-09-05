"""Migration wave planning models."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.project import Project


class MigrationWave(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """A sequenced migration wave within a project."""

    __tablename__ = "migration_waves"
    __table_args__ = (
        UniqueConstraint("project_id", "wave_number", name="uq_migration_waves_project_number"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    external_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    wave_number: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)

    project: Mapped[Project] = relationship(back_populates="migration_waves")
    memberships: Mapped[list[MigrationWaveMembership]] = relationship(back_populates="wave")


class MigrationWaveMembership(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Application membership in a migration wave."""

    __tablename__ = "migration_wave_memberships"
    __table_args__ = (UniqueConstraint("wave_id", "application_id", name="uq_wave_membership_app"),)

    wave_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("migration_waves.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    prerequisites: Mapped[list[str] | None] = mapped_column(ARRAY(String(64)), nullable=True)
    blockers: Mapped[list[str] | None] = mapped_column(ARRAY(String(64)), nullable=True)

    wave: Mapped[MigrationWave] = relationship(back_populates="memberships")
