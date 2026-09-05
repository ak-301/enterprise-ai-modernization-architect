"""SQLAlchemy declarative base.

Domain models (Application, Service, Database, …) are added in Stage 2.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass
