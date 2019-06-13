import unittest

from tests import run_async
from tests.mocks.mock_db import create_test_db

from micro_tcg.storage.user_repo import (
    insert,
    count
)

user_data = dict(
    name='tester',
    token='some_token',
    password='secret_password'
)


class TestInsertUser(unittest.TestCase):

    @run_async
    async def test_returns_the_inserted_id(self):
        db = await create_test_db()
        inserted_id = await insert(db, user_data)
        self.assertIsNotNone(inserted_id)

    @run_async
    async def test_inserts_one_item_in_the_repository(self):
        db = await create_test_db()
        expected = await count(db) + 1
        await insert(db, user_data)
        actual = await count(db)
        self.assertEqual(actual, expected)
