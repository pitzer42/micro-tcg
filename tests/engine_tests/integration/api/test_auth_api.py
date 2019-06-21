from aiohttp.test_utils import unittest_run_loop

from tests.engine_tests.integration.api import EngineAPITestCase

from engine import routes


class AuthAPITestCase(EngineAPITestCase):

    async def setUpAsync(self) -> None:
        await EngineAPITestCase.setUpAsync(self)
        await self.use_case.register_user()

    @unittest_run_loop
    async def test_successful_login(self):
        response = await self.use_case.login()
        json_response = await response.json()

        self.assertEqual(200, response.status)
        self.assertIsNotNone(json_response)
        self.assertIn('token', json_response)

    @unittest_run_loop
    async def test_wrong_username_login(self):
        response = await self.use_case.login_with_wrong_name()
        json_response = await response.json()

        self.assertEqual(200, response.status)
        self.assertIsNotNone(json_response)
        self.assertIn('message', json_response)
        self.assertNotIn('token', json_response)
        self.assertIn('status', json_response)
        self.assertEqual(401, json_response['status'])

    @unittest_run_loop
    async def test_wrong_password_login(self):
        response = await self.use_case.login_with_wrong_password()
        json_response = await response.json()

        self.assertEqual(200, response.status)
        self.assertIsNotNone(json_response)
        self.assertIn('message', json_response)
        self.assertNotIn('token', json_response)
        self.assertIn('status', json_response)
        self.assertEqual(401, json_response['status'])

    @unittest_run_loop
    async def test_successful_access_to_protected_view(self):
        await self.use_case.login()
        doc = dict(
            token=self.use_case.user.token
        )
        response = await self.client.get(
            routes.secret,
            json=doc
        )
        self.assertEqual(200, response.status)

    @unittest_run_loop
    async def test_unsuccessful_access_to_protected_view(self):
        await self.use_case.login_with_wrong_password()
        doc = dict(
            token=self.use_case.user.token
        )
        response = await self.client.get(
            routes.secret,
            json=doc
        )
        self.assertEqual(401, response.status)

    @unittest_run_loop
    async def test_entering_waiting_list(self):
        await self.use_case.login()
        ack = await self.use_case.enter_waiting_list()

        self.assertIsNotNone(self.use_case.socket)
        self.assertIsNotNone(ack)
        self.assertIn('message', ack)
        self.assertIn('status', ack)
        self.assertEqual(200, ack['status'])

    @unittest_run_loop
    async def test_entering_waiting_list_without_authentication(self):
        await self.use_case.login_with_wrong_password()
        ack = await self.use_case.enter_waiting_list()

        self.assertIsNotNone(self.use_case.socket)
        self.assertIsNotNone(ack)
        self.assertIn('message', ack)
        self.assertIn('status', ack)
        self.assertEqual(401, ack['status'])
