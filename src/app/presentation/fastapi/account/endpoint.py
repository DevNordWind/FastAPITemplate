from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi_error_map import ErrorAwareRouter

from app.app.user.dto import UserDTO
from app.app.user.query import GetUserById, GetUserByIdQuery
from app.domain.common.actor import UserActor
from app.infra.presentation.fastapi.handler import (
    RegisterHandler,
    RegisterHandlerData,
)
from app.infra.presentation.fastapi.handler.log_in import (
    LogInHandler,
    LogInHandlerData,
    LogInResultDTO,
)
from app.infra.presentation.fastapi.handler.log_out import (
    LogOutHandler,
    LogOutHandlerData,
)
from app.infra.presentation.fastapi.handler.register import RegisterResultDTO
from app.presentation.fastapi.account.schema import (
    LogInRequest,
    LogInResponse,
    RegisterRequest,
    RegisterResponse,
    User,
)
from app.presentation.fastapi.adapter import HttpActorProvider
from app.presentation.fastapi.schema import GENERAL_ERRORS, OK_RESPONSE, OkResponse
from app.presentation.fastapi.security import SECURITY

account_router = ErrorAwareRouter(prefix="/account", tags=["Account"])


@account_router.post("/register", error_map=GENERAL_ERRORS)
@inject
async def register(
    body: RegisterRequest,
    handler: FromDishka[RegisterHandler],
) -> RegisterResponse:
    result: RegisterResultDTO = await handler.execute(
        data=RegisterHandlerData(
            login=body.login,
            password=body.password,
        )
    )
    return RegisterResponse.from_result(result)


@account_router.post("/login", error_map=GENERAL_ERRORS)
@inject
async def log_in(
    body: LogInRequest,
    handler: FromDishka[LogInHandler],
) -> LogInResponse:
    result: LogInResultDTO = await handler.execute(
        data=LogInHandlerData(
            login=body.login,
            password=body.password,
        )
    )
    return LogInResponse.from_result(result)


@account_router.post("/logout", error_map=GENERAL_ERRORS)
@inject
async def log_out(
    handler: FromDishka[LogOutHandler],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(SECURITY)],
) -> OkResponse:
    await handler.execute(data=LogOutHandlerData(access_token=credentials.credentials))
    return OK_RESPONSE


@account_router.get("/me", error_map=GENERAL_ERRORS, dependencies=[Depends(SECURITY)])
@inject
async def get_me(
    actor_provider: FromDishka[HttpActorProvider], query: FromDishka[GetUserById]
) -> User:
    actor: UserActor = await actor_provider.get()
    user_dto: UserDTO = await query(GetUserByIdQuery(id=actor.id.value))

    return User.from_dto(src=user_dto)
