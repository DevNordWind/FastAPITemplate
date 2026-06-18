from dataclasses import dataclass

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.app.user.exception import UserAuthenticationError
from app.domain.user.exception import UserPermissionDenied
from app.infra.presentation.fastapi.model import AccessToken
from app.infra.presentation.fastapi.port.blacklist_gateway import (
    AccessTokenBlacklistGateway,
)


@dataclass(slots=True, frozen=True)
class LogOutHandlerData:
    access_token: str


class LogOutHandler:
    def __init__(
        self,
        blacklist_gw: AccessTokenBlacklistGateway,
        actor_provider: ActorProvider,
        db_session: DatabaseSession,
    ):
        self._blacklist_gw = blacklist_gw
        self._actor_provider = actor_provider
        self._db_session = db_session

    async def execute(self, data: LogOutHandlerData) -> None:
        try:
            await self._actor_provider.get()
        except UserAuthenticationError:
            raise UserPermissionDenied  # noqa: B904

        await self._blacklist_gw.add(AccessToken(data.access_token))
