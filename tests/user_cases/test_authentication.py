from engine.use_cases.authentication import Authentication

from tests.repositories.user_repo_test_case import UserRepositoryTestCase
from tests.utils import sync


class TestAuthentication(UserRepositoryTestCase):

    @property
    def use_case(self):
        return Authentication(self.users)
    
    @sync
    async def test_successful_authentication(self):
        dummy = await self.insert_dummy()
        authenticated = await self.use_case._authenticate_user(dummy.name, dummy.password)
        self.assertTrue(authenticated)

    @sync
    async def test_unsuccessful_authentication(self):
        dummy = await self.insert_dummy()
        dummy.password = 'wrong_password'
        authenticated = await self.use_case._authenticate_user(dummy.name, dummy.password)
        self.assertFalse(authenticated)

    @sync
    async def test_user_has_a_token_after_login(self):
        dummy = await self.insert_dummy()
        logged_in = await self.use_case.login(dummy.name, dummy.password)
        self.assertTrue(logged_in)

        query_result = await self.users.get_by_name(dummy.name)
        self.assertIsNotNone(query_result.token)

    @sync
    async def test_successful_token_validation(self):
        dummy = await self.insert_dummy()
        dummy.token = await self.use_case.login(dummy.name, dummy.password)
        valid_token = await self.use_case.validate_token(dummy.token)
        self.assertTrue(valid_token)

    @sync
    async def test_successful_token_validation(self):
        fake_token = 'fake_token'
        valid_token = await self.use_case.validate_token(fake_token)
        self.assertFalse(valid_token)

    @sync
    async def test_user_does_not_have_a_token_after_logout(self):
        dummy = await self.insert_dummy()
        dummy.token = await self.use_case.login(dummy.name, dummy.password)
        await self.use_case.logout(dummy.token)
        query_result = await self.users.get_by_name(dummy.name)
        self.assertIsNone(query_result.token)
