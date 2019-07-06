from motor.motor_asyncio import AsyncIOMotorClient


async def create_test_db():
    test_db = AsyncIOMotorClient().micro_tcg_test
    collection_names = await test_db.list_collection_names()
    for collection_name in collection_names:
        await test_db.drop_collection(collection_name)
    return test_db
