from typing import NoReturn

from abc import (
    ABC,
    abstractmethod
)


class RemotePlayer(ABC):

    @abstractmethod
    async def send(self, message: str) -> NoReturn:
        raise NotImplemented()

    @abstractmethod
    async def receive(self) -> str:
        raise NotImplemented()
