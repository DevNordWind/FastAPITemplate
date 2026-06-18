import time

import structlog
from starlette.types import ASGIApp, Receive, Scope, Send

logger = structlog.get_logger(__name__)

_SKIP_PATHS: frozenset[str] = frozenset({"/api/health"})


class StructlogRequestMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path: str = scope.get("path", "")

        if path in _SKIP_PATHS:
            await self.app(scope, receive, send)
            return

        method: str = scope.get("method", "")
        client_ip: str | None = self._get_client_ip(scope)

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            method=method,
            path=path,
            client_ip=client_ip,
        )

        status_code = 500
        start_time = time.perf_counter()

        async def send_wrapper(message: dict) -> None:  # type: ignore[type-arg]
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)  # type: ignore[bad-argument-type]
        except Exception:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            await logger.aerror(
                "request_failed",
                status_code=500,
                duration_ms=duration_ms,
                exc_info=True,
            )
            raise
        else:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            log_method = (
                logger.ainfo
                if status_code < 400  # noqa: PLR2004
                else logger.awarning
                if status_code < 500  # noqa: PLR2004
                else logger.aerror
            )
            await log_method(
                "request_completed",
                status_code=status_code,
                duration_ms=duration_ms,
            )

    @staticmethod
    def _get_client_ip(scope: Scope) -> str | None:
        headers: dict[bytes, bytes] = dict(scope.get("headers", []))
        if xff := headers.get(b"x-forwarded-for"):
            return xff.decode().split(",")[0].strip()
        if xri := headers.get(b"x-real-ip"):
            return xri.decode()
        client = scope.get("client")
        return client[0] if client else None
