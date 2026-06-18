from dataclasses import dataclass
from datetime import datetime
from typing import Final, NewType, override

from app.domain.user.enums import UserRole
from app.domain.user.value_object import UserId
from app.infra.presentation.fastapi.exception import (
    LoginTooLong,
    LoginTooShort,
    PasswordTooLong,
    PasswordTooShort,
)

_MIN_PASSWORD_LENGTH: Final[int] = 6
_MAX_PASSWORD_LENGTH: Final[int] = 64
_MIN_LOGIN_LENGTH: Final[int] = 2
_MAX_LOGIN_LENGTH: Final[int] = 64

PasswordHash = NewType("PasswordHash", str)
AccessToken = NewType("AccessToken", str)


@dataclass(slots=True, frozen=True)
class PasswordRaw:
    value: str

    def __post_init__(self) -> None:
        if len(self.value) < _MIN_PASSWORD_LENGTH:
            raise PasswordTooShort(min_length=_MIN_PASSWORD_LENGTH)
        if len(self.value) > _MAX_PASSWORD_LENGTH:
            raise PasswordTooLong(max_length=_MAX_PASSWORD_LENGTH)

    @override
    def __str__(self) -> str:
        return self.value


@dataclass(slots=True, frozen=True)
class Login:
    value: str

    def __post_init__(self) -> None:
        normalized: str = self.value.strip().title()

        if len(normalized) < _MIN_LOGIN_LENGTH:
            raise LoginTooShort(min_length=_MIN_LOGIN_LENGTH)
        if len(normalized) > _MAX_LOGIN_LENGTH:
            raise LoginTooLong(max_length=_MAX_LOGIN_LENGTH)

        object.__setattr__(self, "value", normalized)

    @override
    def __str__(self) -> str:
        return self.value


@dataclass
class UserCredentials:
    user_id: UserId

    login: Login
    password_hash: PasswordHash

    updated_at: datetime


@dataclass(slots=True, frozen=True)
class UserCredentialsCtx:
    credentials: UserCredentials
    role: UserRole
