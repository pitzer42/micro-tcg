from tests import run_async
from tests.engine_tests.unit.storage.user_repo import TestUserRepo

import engine.storage.user_repo as users


class TestListAllUsers(TestUserRepo):

    @run_async
    async def test_returns_a_list_of_dicts(self):
        all_users = await users.list_all(TestUserRepo.db)
        user = all_users[0]

        self.assertIsInstance(all_users, list)
        self.assertIsInstance(user, dict)

    @run_async
    async def test_limit_result_length(self):
        expected_length = 0
        all_users = await users.list_all(TestUserRepo.db, limit=expected_length)
        length = len(all_users)

        self.assertEqual(length, expected_length)
