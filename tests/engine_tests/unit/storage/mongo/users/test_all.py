from tests import run_async

from tests.engine_tests.unit.storage.mongo.users import TestUsers


class TestListAllUsers(TestUsers):

    @run_async
    async def test_returns_a_list_of_dicts(self):
        all_users = await self.users.all()
        user = all_users[0]

        self.assertIsInstance(all_users, list)
        self.assertIsInstance(user, dict)

    @run_async
    async def test_limit_result_length(self):
        expected_length = 0
        all_users = await self.users.all(limit=expected_length)
        length = len(all_users)

        self.assertEqual(length, expected_length)
