from engine.models.user import User

from tests.utils import sync
from tests.repositories.user_repo_test_case import UserRepositoryTestCase
import tests.mocks.dummy_user_factory as dummies


class TestUserRepository(UserRepositoryTestCase):

    @sync
    async def test_all_returns_a_list_of_users(self):
        users = await self.users.to_list()
        self.assertIsInstance(users, list)
        self.assertGreater(len(users), 0)
        self.assertIsInstance(users[0], User)

    @sync
    async def test_all_limited_to_length(self):
        users = await self.users.to_list(length=0)
        self.assertIsInstance(users, list)
        self.assertEqual(len(users), 0)

    @sync
    async def test_insert_user(self):
        user = dummies.create()
        repo_id = await self.users.insert(user)
        self.assertIsNotNone(repo_id)

    @sync
    async def test_count(self):
        before = await self.users.count()
        await self.insert_dummy()
        after = await self.users.count()
        self.assertEqual(before + 1, after)

    @sync
    async def test_delete(self):
        dummy = await self.insert_dummy()

        query_result = await self.users.get_by_name(dummy.name)
        self.assertEqual(dummy, query_result)

        await self.users.delete_by_name(dummy.name)
        query_result = await self.users.get_by_name(dummy.name)
        self.assertIsNone(query_result)

    @sync
    async def test_password_is_stored_as_hash(self):
        dummy = await self.insert_dummy()
        query_result = await self.users.get_by_name(dummy.name)
        self.assertNotEqual(query_result.password, dummy.password)
