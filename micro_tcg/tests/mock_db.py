from micro_tcg.models import User

from motor.motor_asyncio import AsyncIOMotorClient

default_user_data = dict(
    username='tester',
    email='tester@aiohttp.com',
    password='tester123'
)


async def create_test_db():
    test_db = AsyncIOMotorClient().micro_tcg_test
    User.get_collection(test_db).drop()
    await User(**default_user_data).save(test_db)
    return test_db
