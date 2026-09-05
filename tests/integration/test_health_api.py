"""API integration tests for health endpoints (no DB required for /health)."""

from __future__ import annotations

from unittest.mock import patch

from app.main import create_app
from fastapi.testclient import TestClient


def test_health_endpoint() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "aima-api"
    assert "X-Request-ID" in response.headers


def test_health_endpoint_under_api_prefix() -> None:
    client = TestClient(create_app())
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready_when_db_up() -> None:
    with patch("app.api.routes.health.check_database_connection", return_value=True):
        client = TestClient(create_app())
        response = client.get("/ready")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["components"][0]["name"] == "postgresql"
    assert body["components"][0]["status"] == "up"


def test_ready_when_db_down() -> None:
    with patch(
        "app.api.routes.health.check_database_connection",
        side_effect=ConnectionError("connection refused"),
    ):
        client = TestClient(create_app())
        response = client.get("/ready")
    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "not_ready"
    assert body["components"][0]["status"] == "down"


def test_request_id_propagation() -> None:
    client = TestClient(create_app())
    response = client.get("/health", headers={"X-Request-ID": "test-req-123"})
    assert response.headers["X-Request-ID"] == "test-req-123"
