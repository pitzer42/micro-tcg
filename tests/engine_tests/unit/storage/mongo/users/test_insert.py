from tests import run_async
from tests.engine_tests.unit.repos.users import user_data_without_id
from tests.engine_tests.unit.storage.mongo.users import TestUsers


class TestInsertUser(TestUsers):

    @run_async
    async def test_returns_the_inserted_id(self):
        inserted_id = await self.users.insert(user_data_without_id)

        self.assertIsNotNone(inserted_id)

    @run_async
    async def test_inserts_one_item_in_the_repository(self):
        expected = await self.users.count() + 1
        await self.users.insert(user_data_without_id)
        actual = await self.users.count()

        self.assertEqual(actual, expected)

