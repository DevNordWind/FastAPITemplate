from typing import Final, Literal

from app.presentation.fastapi.schema import BaseSchema


class OkResponse(BaseSchema):
    status: Literal["ok"]


OK_RESPONSE: Final[OkResponse] = OkResponse(status="ok")
