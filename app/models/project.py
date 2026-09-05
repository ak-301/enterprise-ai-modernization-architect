"""Project and portfolio container models."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.application import Application
    from app.models.audit import AuditEvent
    from app.models.dependency import Dependency
    from app.models.document import Document
    from app.models.infrastructure import InfrastructureResource
    from app.models.migration_wave import MigrationWave


class Project(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """A modernization engagement / portfolio container.

    Example: "Acme Financial Services — FY26 Modernization"
    """

    __tablename__ = "projects"

    external_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    organization_name: Mapped[str] = mapped_column(String(255), nullable=False)
    industry: Mapped[str | None] = mapped_column(String(128), nullable=True)

    applications: Mapped[list[Application]] = relationship(back_populates="project")
    infrastructure_resources: Mapped[list[InfrastructureResource]] = relationship(
        back_populates="project"
    )
    dependencies: Mapped[list[Dependency]] = relationship(back_populates="project")
    documents: Mapped[list[Document]] = relationship(back_populates="project")
    migration_waves: Mapped[list[MigrationWave]] = relationship(back_populates="project")
    audit_events: Mapped[list[AuditEvent]] = relationship(back_populates="project")
