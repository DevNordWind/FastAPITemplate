from dataclasses import dataclass
from typing import Final
from uuid import UUID

from app.app.common.port.session import DatabaseSession
from app.app.user.port.reader import UserReader
from app.app.user.service import UserApplicationService
from app.app.user.service.service import RegisterUserData
from app.domain.common.port import Clock
from app.domain.user.enums import UserRole
from app.domain.user.value_object import UserId
from app.infra.presentation.fastapi.model import (
    Login,
    PasswordRaw,
    UserCredentials,
)
from app.infra.presentation.fastapi.port import (
    PasswordHasher,
    TokenProvider,
    UserCredentialsGateway,
)

_DEFAULT_ROLE: Final[UserRole] = UserRole.USER


@dataclass(slots=True, frozen=True)
class RegisterHandlerData:
    login: str
    password: str


@dataclass(slots=True, frozen=True)
class RegisterResultDTO:
    id: UUID

    token: str


class RegisterHandler:
    def __init__(
        self,
        credentials_gateway: UserCredentialsGateway,
        session: DatabaseSession,
        service: UserApplicationService,
        pw_hasher: PasswordHasher,
        token_generator: TokenProvider,
        user_reader: UserReader,
        clock: Clock,
    ):
        self._credentials_gw = credentials_gateway
        self._session = session
        self._pw_hasher = pw_hasher
        self._clock = clock
        self._token_generator = token_generator
        self._user_reader = user_reader
        self._service = service

    async def execute(self, data: RegisterHandlerData) -> RegisterResultDTO:
        password_raw = PasswordRaw(data.password)
        login = Login(data.login)

        user_id: UserId = await self._service.register(
            RegisterUserData(role=_DEFAULT_ROLE)
        )
        now = self._clock.now()
        credentials = UserCredentials(
            user_id=user_id,
            login=login,
            password_hash=self._pw_hasher.hash(password_raw=password_raw),
            updated_at=now,
        )

        await self._credentials_gw.add(credentials=credentials)
        await self._session.commit()

        token = self._token_generator.generate_access(
            user_id=user_id, now=now, role=_DEFAULT_ROLE
        )

        return RegisterResultDTO(
            id=user_id.value,
            token=token,
        )
