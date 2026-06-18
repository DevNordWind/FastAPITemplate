from datetime import UTC, datetime
from typing import Any, Final, override

from redis.asyncio import Redis

from app.domain.common.port import Clock
from app.infra.presentation.fastapi.model import AccessToken
from app.infra.presentation.fastapi.port.blacklist_gateway import (
    AccessTokenBlacklistGateway,
)
from app.infra.presentation.fastapi.port.token import TokenDecoder

_TOKEN_PREFIX: Final[str] = "blacklist:access_token:"  # noqa: S105


class RedisAccessTokenBlacklistGateway(AccessTokenBlacklistGateway):
    def __init__(
        self,
        redis: Redis,
        decoder: TokenDecoder,
        clock: Clock,
        token_prefix: str = _TOKEN_PREFIX,
    ):
        self._redis = redis
        self._decoder = decoder
        self._clock = clock
        self._token_prefix = token_prefix

    @override
    async def add(self, token: AccessToken) -> None:
        payload: dict[str, Any] = self._decoder.decode_access(token=token)
        exp = datetime.fromtimestamp(payload["exp"], UTC)
        ttl: int | float = (exp - self._clock.now()).total_seconds()
        if ttl <= 0:
            return

        await self._redis.set(
            name=self._token_prefix + payload["jti"],
            value=1,
            ex=int(ttl),
        )

    @override
    async def check(self, token: AccessToken) -> bool:
        payload = self._decoder.decode_access(token=token)

        return await self._redis.get(self._token_prefix + payload["jti"]) is not None
