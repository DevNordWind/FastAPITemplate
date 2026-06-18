from app.domain.common.port import Clock, UUIDProvider
from app.domain.user.entity import User
from app.domain.user.enums import UserRole
from app.domain.user.value_object import UserId


class UserDomainService:
    def __init__(self, clock: Clock, uuid_provider: UUIDProvider):
        self._clock = clock
        self._uuid = uuid_provider

    def register(self, role: UserRole) -> User:
        return User(id=UserId(self._uuid()), role=role, reg_at=self._clock.now())
