import uuid
from datetime import datetime
from typing import Any, override

import jwt
from jwt import InvalidTokenError

from app.app.user.exception import UserNotAuthenticatedError
from app.config.auth_policy import AuthPolicyConfig
from app.domain.user.enums import UserRole
from app.domain.user.value_object import UserId
from app.infra.presentation.fastapi.model import AccessToken
from app.infra.presentation.fastapi.port import TokenProvider
from app.infra.presentation.fastapi.port.token import TokenDecoder


class JWTTokenProcessor(TokenProvider, TokenDecoder):
    def __init__(
        self,
        auth_policy_config: AuthPolicyConfig,
    ):
        self._auth_policy_config = auth_policy_config

    @override
    def generate_access(
        self,
        user_id: UserId,
        role: UserRole,
        now: datetime,
    ) -> AccessToken:
        token = jwt.encode(
            payload={
                "sub": user_id.value.hex,
                "role": role.value,
                "exp": now + self._auth_policy_config.expires_in,
                "jti": uuid.uuid7().hex,
            },
            key=self._auth_policy_config.jwt_secret,
            algorithm=self._auth_policy_config.jwt_algorithm,
        )
        return AccessToken(token)

    @override
    def decode_access(self, token: AccessToken) -> dict[str, Any]:
        try:
            return jwt.decode(
                jwt=token,
                key=self._auth_policy_config.jwt_secret,
                algorithms=[self._auth_policy_config.jwt_algorithm],
                options={
                    "require": ["exp", "sub", "jti"],
                    "verify_signature": True,
                    "verify_exp": True,
                },
            )
        except InvalidTokenError as e:
            raise UserNotAuthenticatedError from e
