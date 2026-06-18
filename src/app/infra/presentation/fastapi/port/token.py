from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from app.domain.user.enums import UserRole
from app.domain.user.value_object import UserId
from app.infra.presentation.fastapi.model import AccessToken


class TokenProvider(ABC):
    @abstractmethod
    def generate_access(
        self,
        user_id: UserId,
        role: UserRole,
        now: datetime,
    ) -> AccessToken:
        raise NotImplementedError


class TokenDecoder(ABC):
    @abstractmethod
    def decode_access(
        self,
        token: AccessToken,
    ) -> dict[str, Any]:
        raise NotImplementedError
