from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.session import DatabaseSession
from app.domain.common.port import Clock
from app.infra.presentation.fastapi.exception import (
    InvalidCredentialsError,
    LoginError,
    PasswordError,
)
from app.infra.presentation.fastapi.model import (
    Login,
    PasswordRaw,
    UserCredentialsCtx,
)
from app.infra.presentation.fastapi.port import (
    PasswordHasher,
    TokenProvider,
    UserCredentialsGateway,
)


@dataclass(slots=True, frozen=True)
class LogInHandlerData:
    login: str
    password: str


@dataclass(slots=True, frozen=True)
class LogInResultDTO:
    id: UUID

    token: str


class LogInHandler:
    def __init__(
        self,
        credentials_gw: UserCredentialsGateway,
        pw_hasher: PasswordHasher,
        clock: Clock,
        session: DatabaseSession,
        token_generator: TokenProvider,
    ):
        self._credentials_gw = credentials_gw
        self._pw_hasher = pw_hasher
        self._clock = clock
        self._db_session = session
        self._token_generator = token_generator

    async def execute(self, data: LogInHandlerData) -> LogInResultDTO:
        try:
            login = Login(data.login)
        except LoginError as e:
            raise InvalidCredentialsError from e

        try:
            password_raw = PasswordRaw(data.password)
        except PasswordError as e:
            raise InvalidCredentialsError from e

        ctx: UserCredentialsCtx | None = await self._credentials_gw.get_ctx_by_login(
            login=login
        )

        if not ctx or not self._pw_hasher.verify(
            password_raw=password_raw,
            password_hash=ctx.credentials.password_hash,
        ):
            raise InvalidCredentialsError

        now = self._clock.now()
        token = self._token_generator.generate_access(
            user_id=ctx.credentials.user_id, now=now, role=ctx.role
        )

        return LogInResultDTO(
            id=ctx.credentials.user_id.value,
            token=token,
        )
