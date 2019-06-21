from tests import run_async
from tests.engine_tests.unit.storage.user_repo import (
    TestUserRepo,
    user_data_without_id
)

import engine.storage.user_repo as users


class TestInsertUser(TestUserRepo):

    @run_async
    async def test_returns_the_inserted_id(self):
        db = TestUserRepo.db
        inserted_id = await users.insert(db, user_data_without_id)

        self.assertIsNotNone(inserted_id)

    @run_async
    async def test_inserts_one_item_in_the_repository(self):
        db = TestUserRepo.db
        expected = await users.count(TestUserRepo.db) + 1
        await users.insert(db, user_data_without_id)
        actual = await users.count(TestUserRepo.db)

        self.assertEqual(actual, expected)

