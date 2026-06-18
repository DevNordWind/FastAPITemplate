from collections.abc import Mapping
from types import MappingProxyType

from app.domain.common.exception import DomainError
from app.domain.user.exception.user import UserAlreadyExists


class IntegrityErrorMapper:
    MAPPING: Mapping[str, type[DomainError]] = MappingProxyType(
        {"ix_UserCredentials_login": UserAlreadyExists},
    )

    @classmethod
    def to_domain(cls, constraint: str) -> DomainError | None:
        exc: type[DomainError] | None = cls.MAPPING.get(constraint)
        if not exc:
            return None

        return exc()
