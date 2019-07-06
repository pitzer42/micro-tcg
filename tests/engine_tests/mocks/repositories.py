from tests.engine_tests.mocks.mongo_db import create_test_db
from engine.storage.mongo import MongoRepositories


async def create_test_repositories():
    db = await create_test_db()
    return MongoRepositories(db)
