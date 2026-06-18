from dishka import Provider, Scope, provide, provide_all

from app.app.user.port.reader import UserReader
from app.app.user.query import GetUserById
from app.app.user.service import UserApplicationService
from app.domain.user.port import UserRepository
from app.domain.user.service import UserDomainService
from app.infra.user.reader import SqlAUserReader
from app.infra.user.repository import SqlAUserRepository


class UserDomainServicesProvider(Provider):
    scope = Scope.APP

    service = provide(UserDomainService)


class UserHandlersProvider(Provider):
    scope = Scope.REQUEST

    services = provide_all(UserApplicationService)

    queries = provide_all(GetUserById)


class UserAdaptersProvider(Provider):
    scope = Scope.REQUEST

    repository = provide(SqlAUserRepository, provides=UserRepository)

    reader = provide(SqlAUserReader, provides=UserReader)
