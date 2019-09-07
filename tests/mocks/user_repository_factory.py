from engine.repositories.user_repository import UserRepository
from tests.mocks.mongo_factory import create as create_db
from tests.config import user_repo_factory


async def create() -> UserRepository:
    db = await create_db()
    return user_repo_factory(db)
