"""Service inventory model."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import EnvironmentName
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.application import Application


class Service(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Deployable service belonging to an application."""

    __tablename__ = "services"

    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    external_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    language: Mapped[str | None] = mapped_column(String(128), nullable=True)
    framework: Mapped[str | None] = mapped_column(String(128), nullable=True)
    version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    replicas: Mapped[int | None] = mapped_column(Integer, nullable=True)
    deployment_environment: Mapped[EnvironmentName] = mapped_column(
        Enum(
            EnvironmentName,
            name="environment_name_enum",
            create_constraint=False,
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
        default=EnvironmentName.PRODUCTION,
    )

    application: Mapped[Application] = relationship(back_populates="services")
