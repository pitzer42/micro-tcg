from unittest import TestCase

from engine.repositories.user_repository import UserRepository

from tests.utils import sync
import tests.mocks.dummy_user_factory as dummies
import tests.mocks.user_repository_factory as test_user_repos


class UserRepositoryTestCase(TestCase):

    _users: UserRepository = None

    @property
    def users(self) -> UserRepository:
        return UserRepositoryTestCase._users

    @classmethod
    @sync
    async def setUpClass(cls) -> None:
        # repository backed by a fresh database
        UserRepositoryTestCase._users = await test_user_repos.create()

        # insert dummy entries
        dummy = dummies.create()
        await UserRepositoryTestCase._users.insert(dummy)

    async def insert_dummy(self):
        dummy = dummies.create()
        await self.users.insert(dummy)
        return dummy

