from motor.motor_asyncio import AsyncIOMotorClient
from engine.storage import user_repo


async def create_test_db():
    test_db = AsyncIOMotorClient().micro_tcg_test
    user_repo.get_collection(test_db).drop()
    return test_db
