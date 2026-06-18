from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.app.user.dto import UserDTO
from app.app.user.port.reader import UserReader
from app.domain.user.value_object import UserId
from app.infra.framework.sql_alchemy.table.user import user_table
from app.infra.user.reader.mapper import UserReaderMapper


class SqlAUserReader(UserReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    @override
    async def read_by_id(self, user_id: UserId) -> UserDTO | None:
        stmt = select(user_table.c.id, user_table.c.role, user_table.c.reg_at)

        result = await self._session.execute(stmt)
        row = result.first()
        if not row:
            return None

        return UserReaderMapper.to_dto(row=row)
