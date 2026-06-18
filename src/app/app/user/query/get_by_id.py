from dataclasses import dataclass
from uuid import UUID

from app.app.user.dto import UserDTO
from app.app.user.port.reader import UserReader
from app.domain.user.exception import UserNotFoundError
from app.domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class GetUserByIdQuery:
    id: UUID


class GetUserById:
    def __init__(self, reader: UserReader):
        self._reader = reader

    async def __call__(self, query: GetUserByIdQuery) -> UserDTO:
        user: UserDTO | None = await self._reader.read_by_id(user_id=UserId(query.id))
        if not user:
            raise UserNotFoundError

        return user
