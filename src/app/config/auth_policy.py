import re
from dataclasses import dataclass
from datetime import timedelta
from typing import Final, Literal

from adaptix import P, Provider, loader

JwtAlgorithm = Literal[
    "HS256",
    "HS384",
    "HS512",
    "RS256",
    "RS384",
    "RS512",
    "ES256",
    "ES384",
    "ES512",
    "PS256",
    "PS384",
    "PS512",
    "EdDSA",
]


@dataclass(slots=True, frozen=True, kw_only=True)
class AuthPolicyConfig:
    jwt_secret: str
    jwt_algorithm: JwtAlgorithm = "HS256"
    expires_in: timedelta


_TIMEDELTA_MAPPING: Final[dict[str, str]] = {
    "s": "seconds",
    "m": "minutes",
    "h": "hours",
    "d": "days",
    "w": "weeks",
}

_PATTERN: Final[re.Pattern[str]] = re.compile(r"^(\d+)([smhdw])$")


def timedelta_loader(value: str) -> timedelta:
    match = _PATTERN.fullmatch(value)
    if not match:
        raise ValueError(
            f"Invalid timedelta value '{value}'. Expected format like 30m, 12h, 7d, 2w."
        )

    amount, unit = match.groups()
    return timedelta(**{_TIMEDELTA_MAPPING[unit]: int(amount)})


def auth_policy_loader() -> Provider:
    return loader(P[AuthPolicyConfig].expires_in, timedelta_loader)
