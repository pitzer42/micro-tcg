from motor.motor_asyncio import AsyncIOMotorClient

from tests.utils import sync

from tests.config import test_database_name


async def create():
    db = AsyncIOMotorClient()[test_database_name]
    collection_names = await db.list_collection_names()
    for collection_name in collection_names:
        await db.drop_collection(collection_name)
    return db
