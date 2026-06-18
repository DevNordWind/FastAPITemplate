from dataclasses import dataclass
from datetime import datetime

from app.domain.user.enums import UserRole
from app.domain.user.value_object import UserId


@dataclass
class User:
    id: UserId

    role: UserRole

    reg_at: datetime
