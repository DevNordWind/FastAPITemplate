from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Enum,
    Table,
)
from sqlalchemy.orm import Composite

from app.domain.user.entity import User
from app.domain.user.enums import UserRole
from app.domain.user.value_object import UserId

from .base import mapper_registry, metadata

user_table: Table = Table(
    "User",
    metadata,
    Column("id", UUID, primary_key=True),
    Column(
        "role",
        Enum(UserRole),
        nullable=False,
    ),
    Column("reg_at", DateTime(timezone=True), nullable=False),
)


def map_user() -> None:
    mapper_registry.map_imperatively(
        User,
        user_table,
        properties={
            "id": Composite(UserId, user_table.c.id),
            "_id": user_table.c.id,
        },
    )
