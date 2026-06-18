from dataclasses import dataclass

from app.app.user.exception import UserAuthenticationError


class InvalidCredentialsError(UserAuthenticationError): ...


class CredentialsValidationError(InvalidCredentialsError): ...


class LoginError(CredentialsValidationError): ...


@dataclass
class LoginTooShort(LoginError):
    min_length: int


@dataclass
class LoginTooLong(LoginError):
    max_length: int


class PasswordError(CredentialsValidationError): ...


@dataclass
class PasswordTooShort(PasswordError):
    min_length: int


@dataclass
class PasswordTooLong(PasswordError):
    max_length: int
