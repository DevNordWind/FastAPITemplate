from abc import ABC, abstractmethod

from app.app.user.dto import UserDTO
from app.domain.user.value_object import UserId


class UserReader(ABC):
    @abstractmethod
    async def read_by_id(self, user_id: UserId) -> UserDTO | None:
        raise NotImplementedError
