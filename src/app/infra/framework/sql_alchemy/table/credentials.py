from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
    Table,
)
from sqlalchemy.orm import Composite

from app.domain.user.value_object import UserId
from app.infra.presentation.fastapi.model import Login, UserCredentials

from .base import mapper_registry, metadata

user_credentials_table: Table = Table(
    "UserCredentials",
    metadata,
    Column("user_id", ForeignKey("User.id"), primary_key=True),
    Column("login", String(length=64), nullable=False, index=True, unique=True),
    Column("password_hash", String(length=512), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
)


def map_user_credentials() -> None:
    mapper_registry.map_imperatively(
        UserCredentials,
        user_credentials_table,
        properties={
            "user_id": Composite(UserId, user_credentials_table.c.user_id),
            "_user_id": user_credentials_table.c.user_id,
            "login": Composite(Login, user_credentials_table.c.login),
            "_login": user_credentials_table.c.login,
        },
    )
