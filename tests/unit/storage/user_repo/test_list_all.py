import unittest

from tests import run_async
from tests.mocks.mock_db import create_test_db

from micro_tcg.storage.user_repo import list_all


class TestListAllUsers(unittest.TestCase):

    @run_async
    async def test_returns_a_list_of_dicts(self):
        db = await create_test_db()
        users = await list_all(db)
        user = users[0]
        self.assertIsInstance(users, list)
        self.assertIsInstance(user, dict)

    @run_async
    async def test_limit_result_length(self):
        expected_length = 0
        db = await create_test_db()
        users = await list_all(db, limit=expected_length)
        self.assertEqual(len(users), expected_length)
