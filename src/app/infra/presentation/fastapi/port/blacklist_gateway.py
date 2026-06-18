from abc import ABC, abstractmethod

from app.infra.presentation.fastapi.model import AccessToken


class AccessTokenBlacklistGateway(ABC):
    @abstractmethod
    async def add(self, token: AccessToken) -> None:
        raise NotImplementedError

    @abstractmethod
    async def check(self, token: AccessToken) -> bool:
        raise NotImplementedError
