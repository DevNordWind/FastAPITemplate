import logging
from dataclasses import asdict, dataclass
from typing import Any, override

from fastapi.exceptions import RequestValidationError
from fastapi_error_map import ErrorTranslator, rule
from fastapi_error_map.rules import Rule
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.app.common.exception import (
    AppExternalServiceError,
    AppInfrastructureError,
)
from app.app.user.exception import (
    UserAlreadyAuthenticatedError,
    UserNotAuthenticatedError,
)
from app.domain.common.exception import (
    DomainConflictError,
    DomainPermissionDenied,
    DomainRuleViolation,
    EntityNotFoundError,
    ValueObjectError,
)
from app.infra.presentation.fastapi.exception import (
    CredentialsValidationError,
    InvalidCredentialsError,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ErrorResponse:
    message: str
    detail: dict[str, Any] | None = None


async def request_validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    fields = {}

    for error in exc.errors():
        path = ".".join(map(str, error["loc"][1:]))
        fields[path] = error["msg"]

    response = ErrorResponse(
        message="Validation error",
        detail={
            "fields": fields,
        },
    )

    return JSONResponse(
        status_code=422,
        content=asdict(response),
    )


class Translator(ErrorTranslator[ErrorResponse]):
    @override
    @property
    def error_response_model_cls(self) -> type[ErrorResponse]:
        return ErrorResponse

    @override
    def from_error(self, err: Exception) -> ErrorResponse:
        error_attrs = vars(err)

        return ErrorResponse(message=err.__class__.__name__, detail=error_attrs or None)


def log_on_error(e: Exception) -> None:
    logger.exception(
        "Exception caught\ntype=%s\nmessage=%s\nargs=%s\nattrs=%s",
        type(e).__name__,
        str(e),
        getattr(e, "args", None),
        vars(e) if hasattr(e, "__dict__") else None,
    )


GENERAL_ERRORS: dict[type[Exception], Rule | int] = {
    DomainPermissionDenied: rule(
        status=403,
        translator=Translator(),
    ),
    EntityNotFoundError: rule(status=404, translator=Translator()),
    DomainConflictError: rule(status=409, translator=Translator()),
    DomainRuleViolation: rule(status=422, translator=Translator()),
    ValueObjectError: rule(status=422, translator=Translator()),
    AppExternalServiceError: rule(
        status=502, translator=Translator(), on_error=log_on_error
    ),
    AppInfrastructureError: rule(
        status=500, translator=Translator(), on_error=log_on_error
    ),
    UserAlreadyAuthenticatedError: rule(status=409, translator=Translator()),
    UserNotAuthenticatedError: rule(status=401, translator=Translator()),
    InvalidCredentialsError: rule(status=401, translator=Translator()),
    CredentialsValidationError: rule(status=422, translator=Translator()),
}
