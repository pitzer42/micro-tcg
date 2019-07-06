
from tests import run_async
from tests.engine_tests.unit.repos.users import user_data
from tests.engine_tests.unit.storage.mongo import TestRepositories

from engine.models.user import User


class TestUsers(TestRepositories):

    @run_async
    async def setUp(self) -> None:
        await TestRepositories.setUp(self)
        inserted_id = await self.repositories.users.insert(user_data)
        user_data[User.__id_attr__] = inserted_id
        self.users = self.repositories.users
