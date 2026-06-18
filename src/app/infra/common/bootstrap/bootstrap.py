from app.infra.common.bootstrap.infrastructure import InfrastructureBootstrap


class Bootstrap:
    def __init__(
        self,
        infra_bootstrap: InfrastructureBootstrap,
    ):
        self._infra_bootstrap = infra_bootstrap

    async def check(self) -> None:
        await self._infra_bootstrap.check()
