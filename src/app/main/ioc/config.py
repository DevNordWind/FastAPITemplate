from adaptix import Retort
from dishka import Provider, Scope, provide

from app.config.auth_policy import AuthPolicyConfig
from app.config.configuration import Configuration
from app.config.db import DatabaseConfig
from app.config.log import EnvironmentConfig
from app.config.redis import RedisConfig


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_config(self, retort: Retort) -> Configuration:
        return Configuration.from_yaml(retort=retort)

    @provide
    async def get_db_config(self, config: Configuration) -> DatabaseConfig:
        return config.db

    @provide
    async def get_redis_config(self, config: Configuration) -> RedisConfig:
        return config.redis

    @provide
    async def get_env_config(self, config: Configuration) -> EnvironmentConfig:
        return config.environment

    @provide
    async def get_auth_policy_config(self, config: Configuration) -> AuthPolicyConfig:
        return config.auth_policy
