from typing import Any

from app.app.user.dto import UserDTO


class UserReaderMapper:
    @classmethod
    def to_dto(cls, row: Any) -> UserDTO:
        return UserDTO(id=row.id, role=row.role, reg_at=row.reg_at)
