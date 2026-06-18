from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class InfrastructureBootstrap:
    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        self._session = session
        self._redis = redis

    async def check(self) -> None:
        await self._check_db()
        await self._check_redis()

    async def _check_db(self) -> None:
        try:
            await self._session.execute(text("SELECT 1"))
        except Exception as e:
            raise RuntimeError(f"Connection to database failed: {e}") from e

    async def _check_redis(self) -> None:
        try:
            await self._redis.ping()  # type: ignore[not-async]
        except Exception as e:
            raise RuntimeError(f"Connection to redis failed: {e}") from e
