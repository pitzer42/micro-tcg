from tests import run_async
from tests.unit.storage import user_repo
from tests.unit.storage.user_repo import TestUserRepo
from micro_tcg.storage.user_repo import (
    insert,
    count
)


user_data = dict(user_repo.user_data)
user_data['_id'] = None


class TestInsertUser(TestUserRepo):

    @run_async
    async def test_returns_the_inserted_id(self):
        inserted_id = await insert(TestUserRepo.__db__, user_data)
        self.assertIsNotNone(inserted_id)

    @run_async
    async def test_inserts_one_item_in_the_repository(self):
        expected = await count(TestUserRepo.__db__) + 1
        await insert(TestUserRepo.__db__, user_data)
        actual = await count(TestUserRepo.__db__)
        self.assertEqual(actual, expected)
