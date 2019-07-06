from typing import List, NoReturn

from engine.crypt import encrypt
from engine.models.user import User
from abc import abstractmethod


def clean_up_output(user_data: dict) -> dict:
    clean_data = dict(user_data)
    # remove _id and password from the payload
    del clean_data[User.__id_attr__]
    del clean_data[User.__password_attr__]
    # convert binary into string for easier json encoding
    clean_data[User.__token_attr__] = str(user_data[User.__token_attr__])
    return clean_data


def clean_up_input(user_data: dict) -> dict:
    user_data = dict(user_data)
    password = user_data[User.__password_attr__]
    user_data[User.__password_attr__] = encrypt(password)
    if User.__id_attr__ in user_data and user_data[User.__id_attr__] is None:
        del user_data[User.__id_attr__]
    return user_data


class Users:

    @abstractmethod
    async def get_by_name(self, name: str) -> User:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, user_id: str) -> User:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_token(self, token) -> User:
        raise NotImplementedError()

    @abstractmethod
    async def all(self, limit=100) -> List[User]:
        raise NotImplementedError()

    @abstractmethod
    async def count(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    async def insert(self, user_data: dict) -> str:
        raise NotImplementedError()

    @abstractmethod
    async def set_token(self, user_id: int, token) -> NoReturn:
        raise NotImplementedError()

    @abstractmethod
    async def replace_token(self, old_token, new_token) -> NoReturn:
        raise NotImplementedError()
