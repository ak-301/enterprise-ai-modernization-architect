"""Technology catalog model."""

from __future__ import annotations

from datetime import date

from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Technology(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Technology catalog entry (language, runtime, database engine, etc.)."""

    __tablename__ = "technologies"

    external_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(128), nullable=False)
    vendor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    lifecycle_status: Mapped[str] = mapped_column(String(64), nullable=False, default="supported")
    end_of_support: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
