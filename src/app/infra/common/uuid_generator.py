import uuid
from typing import override
from uuid import UUID

from app.domain.common.port import UUIDProvider


class UUIDProviderImpl(UUIDProvider):
    @override
    def __call__(self) -> UUID:
        return uuid.uuid7()
