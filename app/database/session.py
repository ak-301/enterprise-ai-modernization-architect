"""SQLAlchemy engine and session factory.

Stage 1 only verifies connectivity. Domain models arrive in Stage 2.
"""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config.settings import Settings, get_settings


def create_db_engine(settings: Settings | None = None) -> Engine:
    """Create a SQLAlchemy engine from settings."""
    cfg = settings or get_settings()
    return create_engine(
        cfg.database_url_str,
        pool_size=cfg.database_pool_size,
        max_overflow=cfg.database_max_overflow,
        pool_pre_ping=True,
        future=True,
    )


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Create a sessionmaker bound to the given engine."""
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


# Module-level defaults for FastAPI dependency injection (overridable in tests).
_settings = get_settings()
engine = create_db_engine(_settings)
SessionLocal = create_session_factory(engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_database_connection(db_engine: Engine | None = None) -> bool:
    """Return True if ``SELECT 1`` succeeds against PostgreSQL."""
    target = db_engine or engine
    with target.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True
