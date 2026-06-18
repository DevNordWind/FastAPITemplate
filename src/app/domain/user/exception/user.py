from app.domain.common.exception import (
    DomainConflictError,
    DomainError,
    DomainPermissionDenied,
    EntityNotFoundError,
)


class UserError(DomainError): ...


class UserNotFoundError(UserError, EntityNotFoundError): ...


class UserPermissionDenied(UserError, DomainPermissionDenied): ...


class UserAlreadyExists(UserError, DomainConflictError): ...
