"""HTTP middleware for request correlation and structured access logs."""

from __future__ import annotations

import time
import uuid
from collections.abc import Callable

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.observability.logging import get_logger

logger = get_logger(__name__)


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Attach request_id / trace_id and emit structured request logs."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        trace_id = request.headers.get("x-trace-id") or request_id

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            trace_id=trace_id,
            method=request.method,
            path=request.url.path,
        )

        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            latency_ms = (time.perf_counter() - start) * 1000
            logger.exception(
                "request_failed",
                latency_ms=round(latency_ms, 2),
            )
            raise

        latency_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Trace-ID"] = trace_id

        logger.info(
            "request_completed",
            status_code=response.status_code,
            latency_ms=round(latency_ms, 2),
        )
        return response
