from abc import ABC, abstractmethod

from app.infra.presentation.fastapi.model import PasswordHash, PasswordRaw


class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, password_raw: PasswordRaw) -> PasswordHash:
        raise NotImplementedError

    @abstractmethod
    def verify(self, password_raw: PasswordRaw, password_hash: PasswordHash) -> bool:
        raise NotImplementedError
