from dataclasses import dataclass

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.app.user.exception import (
    UserAlreadyAuthenticatedError,
    UserNotAuthenticatedError,
)
from app.domain.user.entity import User
from app.domain.user.enums import UserRole
from app.domain.user.port import UserRepository
from app.domain.user.service import UserDomainService
from app.domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class RegisterUserData:
    role: UserRole


class UserApplicationService:
    def __init__(
        self,
        service: UserDomainService,
        repo: UserRepository,
        actor_provider: ActorProvider,
        session: DatabaseSession,
    ):
        self._user_service = service
        self._user_repo = repo
        self._actor_provider = actor_provider
        self._session = session

    async def register(self, data: RegisterUserData) -> UserId:
        try:
            await self._actor_provider.get()
        except UserNotAuthenticatedError:
            pass
        else:
            raise UserAlreadyAuthenticatedError

        user: User = self._user_service.register(role=data.role)

        user_id: UserId = user.id
        await self._user_repo.add(user=user)

        return user_id
