from typing import override

from argon2 import PasswordHasher as ArgonHasher

from app.infra.presentation.fastapi.model import PasswordHash, PasswordRaw
from app.infra.presentation.fastapi.port import PasswordHasher


class Argon2PasswordHasher(PasswordHasher):
    def __init__(self, argon_hasher: ArgonHasher):
        self._argon_hasher = argon_hasher

    @override
    def hash(self, password_raw: PasswordRaw) -> PasswordHash:
        hashed: str = self._argon_hasher.hash(
            password=password_raw.value,
        )
        return PasswordHash(hashed)

    @override
    def verify(
        self,
        password_raw: PasswordRaw,
        password_hash: PasswordHash,
    ) -> bool:
        return self._argon_hasher.verify(
            hash=password_hash, password=password_raw.value
        )
