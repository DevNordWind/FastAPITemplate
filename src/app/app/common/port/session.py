from abc import ABC, abstractmethod
from collections.abc import Iterable, Sequence


class DatabaseSession(ABC):
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def flush(self, objects: Sequence[object] | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def refresh(
        self,
        instance: object,
        attribute_names: Iterable[str] | None = None,
        with_for_update: bool | None = None,
    ) -> None:
        raise NotImplementedError
