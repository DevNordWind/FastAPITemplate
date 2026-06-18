from dishka import Provider

from .common import CommonAdaptersProvider
from .config import ConfigProvider
from .framework import (
    RedisProvider,
    RetortProvider,
    SqlAlchemyProvider,
)
from .presentation import FastApiProvider
from .user import (
    UserAdaptersProvider,
    UserDomainServicesProvider,
    UserHandlersProvider,
)

PROVIDERS: tuple[Provider, ...] = (
    UserDomainServicesProvider(),
    UserHandlersProvider(),
    UserAdaptersProvider(),
    ConfigProvider(),
    FastApiProvider(),
    CommonAdaptersProvider(),
    SqlAlchemyProvider(),
    RetortProvider(),
    RedisProvider(),
)
