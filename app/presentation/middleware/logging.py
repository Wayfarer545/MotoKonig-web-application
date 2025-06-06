from __future__ import annotations

import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send


class LoggingContextMiddleware(BaseHTTPMiddleware):
    """Bind request information to structlog contextvars."""

    async def dispatch(self, request: Request, call_next) -> Response:  # pragma: no cover - thin wrapper
        request_id = str(uuid.uuid4())
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            path=request.url.path,
            method=request.method,
        )
        try:
            response = await call_next(request)
            structlog.contextvars.bind_contextvars(status_code=response.status_code)
            return response
        finally:
            structlog.contextvars.clear_contextvars()