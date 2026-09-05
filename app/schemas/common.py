"""Shared Pydantic schema helpers."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    """Base schema that can be built from SQLAlchemy ORM objects."""

    model_config = ConfigDict(from_attributes=True)


class TimestampSchema(BaseModel):
    created_at: datetime
    updated_at: datetime


class ConfidenceField(BaseModel):
    confidence: float = Field(ge=0.0, le=1.0)


class IdSchema(ORMModel):
    id: UUID
