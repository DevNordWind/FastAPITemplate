from datetime import UTC, datetime
from typing import Final, override
from uuid import UUID

import pytest

from app.domain.common.port import Clock, UUIDProvider


class FixedClock(Clock):
    def __init__(self, fixed: datetime) -> None:
        self._fixed = fixed

    @override
    def now(self) -> datetime:
        return self._fixed


FIXED_NOW: Final[datetime] = datetime(2026, 6, 15, 12, 0, 0, tzinfo=UTC)
FIXED_UUID: Final[UUID] = UUID("019ed863-ebdf-7718-8421-dbe3591e67ae")


@pytest.fixture
def clock() -> FixedClock:
    return FixedClock(FIXED_NOW)


@pytest.fixture
def uuid_provider() -> UUIDProvider:
    return lambda: FIXED_UUID
