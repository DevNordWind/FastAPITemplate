from uuid import UUID

from app.app.user.exception import UserNotAuthenticatedError
from app.domain.common.actor import UserActor
from app.domain.user.enums import UserRole
from app.domain.user.value_object import UserId
from app.infra.presentation.fastapi.model import AccessToken
from app.infra.presentation.fastapi.port.blacklist_gateway import (
    AccessTokenBlacklistGateway,
)
from app.infra.presentation.fastapi.port.token import TokenDecoder


class EnsureAuthenticatedHandler:
    def __init__(
        self, token_decoder: TokenDecoder, blacklist_gw: AccessTokenBlacklistGateway
    ):
        self._token_decoder = token_decoder
        self._blacklist_gw = blacklist_gw

    async def execute(self, token: str) -> UserActor:
        access_token = AccessToken(token)

        payload = self._token_decoder.decode_access(token=access_token)
        if await self._blacklist_gw.check(access_token):
            raise UserNotAuthenticatedError

        return UserActor(
            id=UserId(UUID(payload["sub"])), role=UserRole(payload["role"])
        )
