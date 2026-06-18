import logging
import sys
from dataclasses import dataclass

__all__ = ("EnvironmentConfig",)

from typing import Any

import structlog
from asgi_correlation_id import correlation_id


def add_correlation_id(
    logger: Any, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    req_id = correlation_id.get()
    if req_id:
        event_dict["trace_id"] = req_id
    return event_dict


@dataclass(slots=True, frozen=True, kw_only=True)
class EnvironmentConfig:
    prod: bool
    log_level: int = logging.INFO
    cors_origins: list[str]

    def setup_logging(self) -> None:
        timestamper = structlog.processors.TimeStamper(fmt="iso")

        shared_processors: list[Any] = [
            add_correlation_id,
            timestamper,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.stdlib.ExtraAdder(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.ExceptionRenderer(),
        ]

        if self.prod:
            shared_processors.append(
                structlog.processors.CallsiteParameterAdder(
                    [
                        structlog.processors.CallsiteParameter.FILENAME,
                        structlog.processors.CallsiteParameter.LINENO,
                    ]
                )
            )
            formatter = structlog.stdlib.ProcessorFormatter(
                foreign_pre_chain=shared_processors,
                processors=[
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    structlog.processors.JSONRenderer(),
                ],
            )
        else:
            formatter = structlog.stdlib.ProcessorFormatter(
                foreign_pre_chain=shared_processors,
                processors=[
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    structlog.dev.ConsoleRenderer(colors=True),
                ],
            )

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)

        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        root_logger.addHandler(handler)
        root_logger.setLevel(self.log_level)

        for _log in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
            logging.getLogger(_log).handlers.clear()
            logging.getLogger(_log).propagate = True

        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

        structlog.configure(
            processors=[
                *shared_processors,
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

    def add_correlation_id(
        self, logger: Any, method_name: str, event_dict: dict[str, Any]
    ) -> dict[str, Any]:
        req_id = correlation_id.get()
        if req_id:
            event_dict["trace_id"] = req_id
        return event_dict
