from collections.abc import AsyncIterable

import orjson
from adaptix import Retort
from dishka import Provider, Scope, provide
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from app.config.auth_policy import auth_policy_loader
from app.config.db import DatabaseConfig
from app.config.redis import RedisConfig


class RetortProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_retort(self) -> Retort:
        return Retort(
            strict_coercion=False,
            recipe=[auth_policy_loader()],
        )


class SqlAlchemyProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_engine(self, configuration: DatabaseConfig) -> AsyncEngine:
        return create_async_engine(
            url=configuration.connection_str,
            echo=configuration.sql_alchemy.echo,
            hide_parameters=configuration.sql_alchemy.hide_parameters,
            pool_pre_ping=configuration.sql_alchemy.pool_pre_ping,
            json_serializer=lambda obj: orjson.dumps(obj).decode(),
            json_deserializer=orjson.loads,
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        engine: AsyncEngine,
    ) -> AsyncIterable[AsyncSession]:
        async with AsyncSession(engine) as session:
            yield session


class RedisProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_redis(self, configuration: RedisConfig) -> Redis:
        return Redis(
            db=configuration.db,
            host=configuration.host,
            username=configuration.username,
            password=configuration.password,
            port=configuration.port,
            decode_responses=True,
        )
