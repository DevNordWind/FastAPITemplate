from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.user.enums import UserRole


@dataclass(slots=True, frozen=True)
class UserDTO:
    id: UUID

    role: UserRole

    reg_at: datetime
