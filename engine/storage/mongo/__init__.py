from engine.repos import Repositories
from engine.storage.mongo.users import MongoUsers
from motor.motor_asyncio import AsyncIOMotorClient


class MongoRepositories(Repositories):

    def __init__(self, mongo_db: AsyncIOMotorClient):
        self._users = MongoUsers(mongo_db)
