import asyncio

from polls.models import User
from motor.motor_asyncio import AsyncIOMotorClient


async def main():
    db = AsyncIOMotorClient().micro_tcg

    new_user = User(
        username='test_user',
        email='test_user@aiohtttp.com',
        password='password123'
    )

    return await new_user.save(db)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([main()]))
    loop.close()
