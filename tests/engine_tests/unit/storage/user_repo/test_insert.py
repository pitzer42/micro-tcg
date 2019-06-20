from tests.engine_tests import run_async
from tests.engine_tests.unit.storage import user_repo
from tests.engine_tests.unit.storage.user_repo import TestUserRepo

from engine.storage.user_repo import (
    insert,
    count
)


user_data = dict(user_repo.user_data)
user_data['_id'] = None


class TestInsertUser(TestUserRepo):

    @run_async
    async def test_returns_the_inserted_id(self):
        db = TestUserRepo._db
        inserted_id = await insert(db, user_data)
        self.assertIsNotNone(inserted_id)

    @run_async
    async def test_inserts_one_item_in_the_repository(self):
        db = TestUserRepo._db
        expected = await count(TestUserRepo._db) + 1
        await insert(db, user_data)
        actual = await count(TestUserRepo._db)
        self.assertEqual(actual, expected)

