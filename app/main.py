"""FastAPI application factory."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import health
from app.config.settings import get_settings
from app.observability.logging import configure_logging, get_logger
from app.observability.middleware import RequestContextMiddleware

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Application startup / shutdown hooks."""
    settings = get_settings()
    configure_logging(settings.log_level, settings.log_format)
    logger.info(
        "application_starting",
        service=settings.service_name,
        environment=settings.environment,
        version="0.1.0",
    )
    yield
    logger.info("application_shutdown")


def create_app() -> FastAPI:
    """Build and return the FastAPI application."""
    settings = get_settings()

    application = FastAPI(
        title="Enterprise AI Modernization Architect",
        description=(
            "Enterprise AI Modernization Architect. "
            "Evidence-grounded modernization recommendations for legacy portfolios. "
            "Synthetic demo data only — not a production migration executor."
        ),
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    application.add_middleware(RequestContextMiddleware)
    application.include_router(health.router)
    application.include_router(health.router, prefix=settings.api_prefix)

    return application


app = create_app()
