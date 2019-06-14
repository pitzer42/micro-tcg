from tests import run_async
from tests.unit.storage.user_repo import TestUserRepo
from micro_tcg.storage.user_repo import list_all


class TestListAllUsers(TestUserRepo):

    @run_async
    async def test_returns_a_list_of_dicts(self):
        users = await list_all(TestUserRepo.__db__)
        user = users[0]
        self.assertIsInstance(users, list)
        self.assertIsInstance(user, dict)

    @run_async
    async def test_limit_result_length(self):
        expected_length = 0
        users = await list_all(TestUserRepo.__db__, limit=expected_length)
        self.assertEqual(len(users), expected_length)
