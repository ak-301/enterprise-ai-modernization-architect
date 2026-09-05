"""Health and readiness endpoints.

``/health`` — liveness (process up).
``/ready``  — readiness (dependencies reachable).
"""

from __future__ import annotations

from fastapi import APIRouter, Response, status

from app.config.settings import get_settings
from app.database.session import check_database_connection
from app.observability.logging import get_logger
from app.schemas.health import ComponentHealth, HealthResponse, ReadinessResponse

router = APIRouter(tags=["health"])
logger = get_logger(__name__)

APP_VERSION = "0.1.0"


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Liveness probe — does not check dependencies."""
    settings = get_settings()
    return HealthResponse(
        service=settings.service_name,
        environment=settings.environment,
        version=APP_VERSION,
    )


@router.get("/ready", response_model=ReadinessResponse)
def ready(response: Response) -> ReadinessResponse:
    """Readiness probe — verifies PostgreSQL connectivity."""
    settings = get_settings()
    components: list[ComponentHealth] = []

    db_status: ComponentHealth
    try:
        check_database_connection()
        db_status = ComponentHealth(name="postgresql", status="up")
    except Exception as exc:
        logger.warning("database_readiness_failed", error=str(exc))
        db_status = ComponentHealth(
            name="postgresql",
            status="down",
            detail=str(exc),
        )
    components.append(db_status)

    all_up = all(c.status == "up" for c in components)
    if not all_up:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return ReadinessResponse(
        status="ready" if all_up else "not_ready",
        service=settings.service_name,
        environment=settings.environment,
        version=APP_VERSION,
        components=components,
    )
