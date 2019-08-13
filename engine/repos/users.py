from typing import List, NoReturn

from engine.crypt import encrypt
from engine.models.user import User
from engine.repos.schemas.user import (
    uid_attr,
    password_attr,
    token_attr
)
from abc import abstractmethod


def clean_up_output(user_data: dict) -> dict:
    clean_data = dict(user_data)
    # remove _id and password from the payload
    del clean_data[uid_attr]
    del clean_data[password_attr]
    # convert binary into string for json encoding
    if token_attr in clean_data:
        clean_data[token_attr] = str(user_data[token_attr])
    return clean_data


def clean_up_input(user_data: dict) -> dict:
    user_data = dict(user_data)
    password = user_data[password_attr]
    user_data[password] = encrypt(password)
    if uid_attr in user_data and user_data[uid_attr] is None:
        del user_data[uid_attr]
    return user_data


class Users:

    @abstractmethod
    async def get_by_name(self, name: str) -> User:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, uid: str) -> User:
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
    async def set_token(self, uid: int, token) -> NoReturn:
        raise NotImplementedError()

    @abstractmethod
    async def replace_token(self, old_token, new_token) -> NoReturn:
        raise NotImplementedError()
