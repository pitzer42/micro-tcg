from aiohttp.test_utils import unittest_run_loop

from tests.engine_tests.integration.api import EngineAPITestCase


class UsersAPITest(EngineAPITestCase):

    @unittest_run_loop
    async def test_get_all_users_json(self):
        response = await self.use_case.get_all_users()
        json_response = await response.json()

        self.assertEqual(200, response.status)
        self.assertIsNotNone(json_response)
        self.assertGreater(len(json_response), 0)

    @unittest_run_loop
    async def test_put_user_json(self):
        response = await self.use_case.register_user()
        json_response = await response.json()

        self.assertEqual(200, response.status)
        self.assertIsNotNone(json_response)
