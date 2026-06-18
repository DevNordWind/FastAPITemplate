import pytest

from app.domain.common.port import Clock, UUIDProvider
from app.domain.user.entity import User
from app.domain.user.enums import UserRole
from app.domain.user.service import UserDomainService
from app.domain.user.value_object import UserId
from tests.unit.conftest import FIXED_NOW, FIXED_UUID


@pytest.fixture
def user_domain_service(clock: Clock, uuid_provider: UUIDProvider) -> UserDomainService:
    return UserDomainService(clock=clock, uuid_provider=uuid_provider)


class TestUserDomainServiceRegister:
    def test_register_returns_fully_constructed_user(
        self, user_domain_service: UserDomainService
    ) -> None:
        role = UserRole.ADMIN

        user = user_domain_service.register(role=role)

        assert user == User(id=UserId(FIXED_UUID), role=role, reg_at=FIXED_NOW)
