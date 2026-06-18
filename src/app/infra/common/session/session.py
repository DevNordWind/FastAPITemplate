import logging
from collections.abc import Iterable, Sequence
from typing import Any, override

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.app.common.port.session import DatabaseSession
from app.domain.common.exception import DomainError
from app.infra.common.session.mapper import IntegrityErrorMapper

logger = logging.getLogger(__name__)


class SqlADatabaseSession(DatabaseSession):
    def __init__(self, session: AsyncSession):
        self.__session: AsyncSession = session

    @override
    async def commit(self) -> None:
        try:
            await self.__session.commit()
        except IntegrityError as e:
            constraint: str | None = getattr(
                e.orig.diag,  # type: ignore[missing-attribute]
                "constraint_name",
                None,
            )
            if constraint is None:
                raise
            domain_error: DomainError | None = IntegrityErrorMapper.to_domain(
                constraint=constraint
            )
            if not domain_error:
                logger.error(
                    "Unmapped DB constraint violated: %s | %s",
                    constraint,
                    str(e),
                )
                raise
            raise domain_error from e

    @override
    async def flush(self, objects: Sequence[Any] | None = None) -> None:
        await self.__session.flush(objects)

    @override
    async def rollback(self) -> None:
        await self.__session.rollback()

    @override
    async def refresh(
        self,
        instance: object,
        attribute_names: Iterable[str] | None = None,
        with_for_update: bool | None = None,
    ) -> None:
        await self.__session.refresh(instance, attribute_names, with_for_update)
