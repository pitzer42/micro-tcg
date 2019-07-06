from typing import List, NoReturn

from engine.repos.users import (
    Users,
    clean_up_input,
    clean_up_output
)
from engine.models.user import User
from motor.motor_asyncio import AsyncIOMotorClient

__collection_name__ = 'users'


class MongoUsers(Users):

    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = db[__collection_name__]

    async def all(self, limit=100) -> List[User]:
        cursor = self.collection.find()
        users_data = await cursor.to_list(length=limit)
        return [clean_up_output(u) for u in users_data]

    async def count(self) -> int:
        query = dict()
        return await self.collection.count_documents(query)

    async def get_by_id(self, user_id: str) -> User:
        return await self.collection.find_one({
            User.__id_attr__: user_id
        })

    async def get_by_name(self, name: str) -> User:
        return await self.collection.find_one({
            User.__name_attr__: name
        })

    async def get_by_token(self, token) -> User:
        return await self.collection.find_one({
            User.__token_attr__: token
        })

    async def set_token(self, user_id: int, token) -> NoReturn:
        query = {
            User.__id_attr__: user_id
        }
        update = {
            '$set': {
                User.__token_attr__: token
            }
        }
        return await self.collection.update_one(query, update)

    async def replace_token(self, old_token, new_token) -> NoReturn:
        query = {
            User.__token_attr__: old_token
        }
        update = {
            '$set': {
                User.__token_attr__: new_token
            }
        }
        return await self.collection.update_one(query, update)

    async def insert(self, user_data: dict) -> str:
        user_data = clean_up_input(user_data)
        result = await self.collection.insert_one(user_data)
        return result.inserted_id
