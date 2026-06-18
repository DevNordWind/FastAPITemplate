from dataclasses import dataclass
from pathlib import Path

import yaml
from adaptix import Retort

from .auth_policy import AuthPolicyConfig
from .db import DatabaseConfig
from .log import EnvironmentConfig
from .redis import RedisConfig


@dataclass(frozen=True, slots=True)
class Configuration:
    db: DatabaseConfig
    redis: RedisConfig
    environment: EnvironmentConfig

    auth_policy: AuthPolicyConfig

    @classmethod
    def from_yaml(
        cls, retort: Retort, path: Path = Path("./config.yaml")
    ) -> Configuration:
        with path.open() as config_file:
            raw = yaml.safe_load(config_file)

        return cls(
            environment=retort.load(raw["environment"], EnvironmentConfig),
            db=retort.load(raw["db"], DatabaseConfig),
            redis=retort.load(raw["redis"], RedisConfig),
            auth_policy=retort.load(raw["auth_policy"], AuthPolicyConfig),
        )
