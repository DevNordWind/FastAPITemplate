from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.framework.sql_alchemy.table.credentials import (
    user_credentials_table,
)
from app.infra.framework.sql_alchemy.table.user import user_table
from app.infra.presentation.fastapi.model import (
    Login,
    UserCredentials,
    UserCredentialsCtx,
)
from app.infra.presentation.fastapi.port import (
    UserCredentialsGateway,
)


class SqlAUserCredentialsGateway(UserCredentialsGateway):
    def __init__(self, session: AsyncSession):
        self._session = session

    @override
    async def add(self, credentials: UserCredentials) -> None:
        self._session.add(credentials)

    @override
    async def get_ctx_by_login(self, login: Login) -> UserCredentialsCtx | None:
        stmt = (
            select(UserCredentials, user_table.c.role)
            .join(user_table, user_table.c.id == user_credentials_table.c.user_id)
            .where(user_credentials_table.c.login == login.value)
        )
        result = await self._session.execute(stmt)
        row = result.first()
        if not row:
            return None

        return UserCredentialsCtx(credentials=row[0], role=row[1])
