from typing import List, NoReturn

from motor.motor_asyncio import AsyncIOMotorClient

from engine.models.user import User
from engine.repositories.user_repository import UserRepository
import engine.repositories.schemas.user_schema as schema
from engine.repositories.data_ports import (
    dict_to_user,
    user_to_password_hashed_dict
)


class MongoUserRepository(UserRepository):

    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = self.db[schema.collection]

    async def to_list(self, length=100, data_port=dict_to_user) -> List:
        cursor = self.collection.find()
        result = await cursor.to_list(length=length)
        return [data_port(item) for item in result]

    async def count(self) -> int:
        query_all = dict()
        return await self.collection.count_documents(query_all)

    async def insert(self, user: User, data_port=user_to_password_hashed_dict) -> NoReturn:
        result = data_port(user)
        return await self.collection.insert_one(result)

    async def get_by_name(self, name: str, data_port=dict_to_user) -> User:
        query = {schema.name: name}
        result = await self.collection.find_one(query)
        return data_port(result) if result is not None else result

    async def delete_by_name(self, name: str) -> NoReturn:
        query = {schema.name: name}
        return await self.collection.delete_one(query)

    async def set_token(self, name: str, token: str) -> NoReturn:
        query = {schema.name: name}
        command = {'$set': {schema.token: token}}
        await self.collection.update_one(query, command)

    async def delete_token(self, token: str) -> NoReturn:
        query = {schema.token: token}
        command = {'$set': {schema.token: None}}
        await self.collection.update_one(query, command)

    async def get_by_token(self, token: str, data_port=dict_to_user) -> User:
        query = {schema.token: token}
        result = await self.collection.find_one(query)
        return data_port(result) if result is not None else result

