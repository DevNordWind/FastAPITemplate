from contextlib import asynccontextmanager
from typing import Final

from adaptix import Retort
from asgi_correlation_id import CorrelationIdMiddleware
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config.auth_policy import auth_policy_loader
from app.config.configuration import Configuration
from app.infra.common.bootstrap import Bootstrap
from app.infra.framework.sql_alchemy.table import map_all
from app.main.ioc import PROVIDERS
from app.presentation.fastapi.main_router import make_main_router
from app.presentation.fastapi.middleware import StructlogRequestMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: AsyncContainer = app.state.dishka_container
    async with container() as scope:
        bootstrap = await scope.get(Bootstrap)
        await bootstrap.check()

    yield
    await container.close()


def app() -> FastAPI:
    map_all()
    container: AsyncContainer = make_async_container(*PROVIDERS)
    config: Final[Configuration] = Configuration.from_yaml(
        retort=Retort(strict_coercion=False, recipe=[auth_policy_loader()]),
    )
    config.environment.setup_logging()

    is_prod = config.environment.prod

    app = FastAPI(
        lifespan=lifespan,
        title="FastAPITemplate",
        docs_url=None if is_prod else "/docs",
        redoc_url=None if is_prod else "/redoc",
        openapi_url=None if is_prod else "/openapi.json",
    )

    app.add_middleware(StructlogRequestMiddleware)
    app.add_middleware(CorrelationIdMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.environment.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    app.include_router(make_main_router(app))
    setup_dishka(container, app)
    return app
