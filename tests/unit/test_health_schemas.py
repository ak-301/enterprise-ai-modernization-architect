"""Unit tests for health schemas and logging configuration."""

from app.observability.logging import configure_logging, get_logger
from app.schemas.health import ComponentHealth, HealthResponse, ReadinessResponse


def test_health_response_schema() -> None:
    response = HealthResponse(service="aima-api", environment="local")
    assert response.status == "ok"
    assert response.version == "0.1.0"


def test_readiness_response_schema() -> None:
    response = ReadinessResponse(
        status="ready",
        service="aima-api",
        environment="local",
        components=[ComponentHealth(name="postgresql", status="up")],
    )
    assert response.status == "ready"
    assert len(response.components) == 1


def test_configure_logging_does_not_raise() -> None:
    configure_logging(log_level="INFO", log_format="console")
    log = get_logger("test")
    log.info("test_event", ok=True)
