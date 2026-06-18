from dishka import Provider, Scope, provide

from app.app.common.port.session import DatabaseSession
from app.domain.common.port import Clock, UUIDProvider
from app.infra.common.bootstrap import (
    Bootstrap,
    InfrastructureBootstrap,
)
from app.infra.common.clock import SystemClock
from app.infra.common.session import SqlADatabaseSession
from app.infra.common.uuid_generator import UUIDProviderImpl


class CommonAdaptersProvider(Provider):
    uuid_generator = provide(UUIDProviderImpl, provides=UUIDProvider, scope=Scope.APP)

    clock = provide(SystemClock, provides=Clock, scope=Scope.APP)

    session = provide(
        SqlADatabaseSession, provides=DatabaseSession, scope=Scope.REQUEST
    )

    infra_bootstrap = provide(InfrastructureBootstrap, scope=Scope.REQUEST)

    bootstrap = provide(Bootstrap, scope=Scope.REQUEST)
