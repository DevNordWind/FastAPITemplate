from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi_error_map import ErrorAwareRouter

from app.presentation.fastapi.account import account_router
from app.presentation.fastapi.health import health_router
from app.presentation.fastapi.schema import request_validation_error_handler

main_router: APIRouter = ErrorAwareRouter(
    prefix="/api/v1",
)


def make_main_router(app: FastAPI) -> APIRouter:
    main_router.include_router(account_router)
    main_router.include_router(health_router)
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)  # type: ignore[bad-argument-type]
    return main_router
