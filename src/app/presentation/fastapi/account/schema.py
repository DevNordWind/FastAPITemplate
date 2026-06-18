from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.app.user.dto import UserDTO
from app.domain.user.enums import UserRole
from app.infra.presentation.fastapi.handler import LogInResultDTO
from app.infra.presentation.fastapi.handler.register import RegisterResultDTO
from app.presentation.fastapi.schema import BaseSchema


class RegisterRequest(BaseSchema):
    login: str
    password: str


class RegisterResponse(BaseSchema):
    id: UUID
    token: str

    @classmethod
    def from_result(
        cls,
        result: RegisterResultDTO,
    ) -> RegisterResponse:
        return cls(
            id=result.id,
            token=result.token,
        )


class LogInRequest(BaseSchema):
    login: str
    password: str


class LoggedUser(BaseSchema):
    id: UUID
    login: str
    name: str
    generations_balance: int = Field(..., alias="generationsBalance")


class LogInResponse(BaseSchema):
    id: UUID
    token: str

    @classmethod
    def from_result(
        cls,
        result: LogInResultDTO,
    ) -> LogInResponse:
        return cls(
            id=result.id,
            token=result.token,
        )


class User(BaseSchema):
    id: UUID

    role: UserRole

    reg_at: datetime

    @classmethod
    def from_dto(cls, src: UserDTO) -> User:
        return User(id=src.id, role=src.role, reg_at=src.reg_at)
