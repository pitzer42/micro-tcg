from typing import (
    NoReturn,
    List
)

from abc import (
    ABC,
    abstractmethod
)

from engine.models.user import User
from engine.repositories.data_ports import pass_by


class UserRepository(ABC):

    @abstractmethod
    async def to_list(self, length=100, data_port=pass_by) -> List:
        raise NotImplemented()

    @abstractmethod
    async def count(self) -> int:
        raise NotImplemented()

    @abstractmethod
    async def insert(self, user: User, data_port=pass_by) -> NoReturn:
        raise NotImplemented()

    @abstractmethod
    async def get_by_name(self, name: str, data_port=pass_by) -> User:
        raise NotImplemented()

    @abstractmethod
    async def get_by_token(self, token: str, data_port=pass_by) -> User:
        raise NotImplemented()

    @abstractmethod
    async def delete_by_name(self, name: str) -> NoReturn:
        raise NotImplemented()

    @abstractmethod
    async def delete_token(self, token: str) -> NoReturn:
        raise NotImplemented()

    @abstractmethod
    async def set_token(self, name: str, token: str) -> NoReturn:
        raise NotImplemented()
