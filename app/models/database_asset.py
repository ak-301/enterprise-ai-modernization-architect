"""Database / datastore inventory model."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import Criticality
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.application import Application


class DatabaseAsset(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Database or datastore associated with an application.

    Named DatabaseAsset (table: database_assets) to avoid clashing with
    the ``app.database`` package.
    """

    __tablename__ = "database_assets"

    application_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("applications.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    external_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    database_type: Mapped[str] = mapped_column(String(128), nullable=False)
    version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    size_gb: Mapped[float | None] = mapped_column(Float, nullable=True)
    table_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    daily_growth_gb: Mapped[float | None] = mapped_column(Float, nullable=True)
    criticality: Mapped[Criticality] = mapped_column(
        Enum(
            Criticality,
            name="criticality_enum",
            create_constraint=False,
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
        default=Criticality.MEDIUM,
    )
    contains_sensitive_data: Mapped[bool] = mapped_column(default=False, nullable=False)

    application: Mapped[Application | None] = relationship(back_populates="databases")
