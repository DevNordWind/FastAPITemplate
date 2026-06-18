from typing import override

from starlette.requests import Request

from app.app.common.port.actor_provider import ActorProvider
from app.app.user.exception import UserNotAuthenticatedError
from app.domain.common.actor import UserActor
from app.infra.presentation.fastapi.handler.ensure_auth import (
    EnsureAuthenticatedHandler,
)


class HttpActorProvider(ActorProvider):
    def __init__(self, request: Request, handler: EnsureAuthenticatedHandler):
        self._req = request
        self._handler = handler

    @override
    async def get(self) -> UserActor:
        token: str = self._extract_from_headers()

        return await self._handler.execute(token=token)

    def _extract_from_headers(self) -> str:
        authorization = self._req.headers.get("authorization")

        if not authorization:
            raise UserNotAuthenticatedError
        try:
            scheme, token = authorization.split()
        except ValueError as e:
            raise UserNotAuthenticatedError from e

        if scheme.lower() != "bearer":
            raise UserNotAuthenticatedError

        return token
