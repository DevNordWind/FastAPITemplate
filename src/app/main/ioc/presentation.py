from argon2 import PasswordHasher as ArgonHasher
from dishka import AnyOf, Scope, provide, provide_all
from dishka.integrations.fastapi import FastapiProvider
from redis.asyncio import Redis

from app.app.common.port.actor_provider import ActorProvider
from app.config.auth_policy import AuthPolicyConfig
from app.domain.common.port import Clock
from app.infra.presentation.fastapi.adapter import (
    Argon2PasswordHasher,
    JWTTokenProcessor,
    RedisAccessTokenBlacklistGateway,
    SqlAUserCredentialsGateway,
)
from app.infra.presentation.fastapi.handler import (
    RegisterHandler,
)
from app.infra.presentation.fastapi.handler.ensure_auth import (
    EnsureAuthenticatedHandler,
)
from app.infra.presentation.fastapi.handler.log_in import LogInHandler
from app.infra.presentation.fastapi.handler.log_out import LogOutHandler
from app.infra.presentation.fastapi.port import (
    AccessTokenBlacklistGateway,
    PasswordHasher,
    TokenDecoder,
    TokenProvider,
    UserCredentialsGateway,
)
from app.presentation.fastapi.adapter import (
    HttpActorProvider,
)


class FastApiProvider(FastapiProvider):
    scope = Scope.REQUEST

    credentials_gateway = provide(
        SqlAUserCredentialsGateway, provides=UserCredentialsGateway
    )

    @provide(scope=Scope.APP)
    async def get_argon_hasher(self) -> ArgonHasher:
        return ArgonHasher()

    hasher = provide(Argon2PasswordHasher, provides=PasswordHasher, scope=Scope.APP)

    handlers = provide_all(
        LogInHandler, RegisterHandler, LogOutHandler, EnsureAuthenticatedHandler
    )

    actor_provider = provide(
        HttpActorProvider,
        provides=AnyOf[HttpActorProvider, ActorProvider],
    )

    @provide(scope=Scope.APP)
    async def get_blacklist_gw(
        self, redis: Redis, decoder: TokenDecoder, clock: Clock
    ) -> AccessTokenBlacklistGateway:
        return RedisAccessTokenBlacklistGateway(
            redis=redis, decoder=decoder, clock=clock
        )

    @provide(scope=Scope.APP)
    async def get_token_processor(
        self, config: AuthPolicyConfig
    ) -> AnyOf[TokenDecoder, TokenProvider]:
        return JWTTokenProcessor(auth_policy_config=config)
