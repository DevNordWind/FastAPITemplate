from abc import ABC, abstractmethod

from app.infra.presentation.fastapi.model import (
    Login,
    UserCredentials,
    UserCredentialsCtx,
)


class UserCredentialsGateway(ABC):
    @abstractmethod
    async def add(self, credentials: UserCredentials) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_ctx_by_login(self, login: Login) -> UserCredentialsCtx | None:
        raise NotImplementedError
