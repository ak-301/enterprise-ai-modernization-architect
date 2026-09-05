"""Health and readiness response schemas."""

from typing import Literal

from pydantic import BaseModel, Field


class ComponentHealth(BaseModel):
    """Health status of a single dependency."""

    name: str
    status: Literal["up", "down"]
    detail: str | None = None


class HealthResponse(BaseModel):
    """Liveness response — process is running."""

    status: Literal["ok"] = "ok"
    service: str
    environment: str
    version: str = Field(default="0.1.0")


class ReadinessResponse(BaseModel):
    """Readiness response — process can serve traffic."""

    status: Literal["ready", "not_ready"]
    service: str
    environment: str
    version: str = Field(default="0.1.0")
    components: list[ComponentHealth]
