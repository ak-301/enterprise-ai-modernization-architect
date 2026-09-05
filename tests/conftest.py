"""Shared pytest fixtures for database-backed tests."""

from __future__ import annotations

# Ensure all models are registered on Base.metadata
import app.models  # noqa: F401
import pytest
from app.database.base import Base
from app.database.session import SessionLocal, engine
from sqlalchemy.orm import Session


@pytest.fixture(scope="session", autouse=True)
def create_schema() -> None:
    """Create tables for integration tests if migrations were not applied yet."""
    Base.metadata.create_all(bind=engine)


@pytest.fixture()
def db_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
