from fastapi_error_map import ErrorAwareRouter

from app.presentation.fastapi.schema import (
    GENERAL_ERRORS,
    OK_RESPONSE,
    OkResponse,
)

health_router = ErrorAwareRouter(prefix="/health", tags=["Health"])


@health_router.get("/", error_map=GENERAL_ERRORS)
async def health() -> OkResponse:
    return OK_RESPONSE
