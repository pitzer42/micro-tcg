from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from micro_tcg.main import create_app
from micro_tcg.tests.mock_db import create_test_db, default_user_data
from micro_tcg import routes


class TestApp(AioHTTPTestCase):

    async def get_application(self):
        test_db = await create_test_db()
        return create_app(db=test_db)

    @unittest_run_loop
    async def test_get_users(self):
        resp = await self.client.get(routes.users)
        self.assertEqual(200, resp.status)
        json_response = await resp.json()
        self.assertIsNotNone(json_response)
        self.assertGreater(len(json_response), 0)

    @unittest_run_loop
    async def test_put_user(self):
        request_data = dict(
            username='test_put_user',
            email='test_put_user@aiohtp.com',
            password='test_put_user_123'
        )
        resp = await self.client.put(routes.users, json=request_data)
        self.assertEqual(200, resp.status)
        json_response = await resp.json()
        self.assertIsNotNone(json_response)

    @unittest_run_loop
    async def test_successful_login(self):
        credentials = dict(
            username=default_user_data['username'],
            password=default_user_data['password']
        )
        resp = await self.client.get(routes.login, json=credentials)
        self.assertEqual(200, resp.status)
        json_response = await resp.json()
        self.assertIsNotNone(json_response)
        self.assertIn('token', json_response)

    @unittest_run_loop
    async def test_unsuccessful_login(self):
        credentials = dict(
            username=default_user_data['username'],
            password=default_user_data['password'] + 'wrong'
        )
        resp = await self.client.get(routes.login, json=credentials)
        json_response = await resp.json()
        self.assertIsNotNone(json_response)
        self.assertIn('message', json_response)
        self.assertNotIn('token', json_response)

    @unittest_run_loop
    async def test_successful_access_to_protected_view(self):
        credentials = dict(
            username=default_user_data['username'],
            password=default_user_data['password']
        )
        resp = await self.client.get(routes.login, json=credentials)
        json_response = await resp.json()
        resp = await self.client.get(routes.secret, json=json_response)
        self.assertEqual(200, resp.status)

    @unittest_run_loop
    async def test_unsuccessful_access_to_protected_view(self):
        credentials = dict(
            token='invalid_token'
        )
        resp = await self.client.get(routes.secret, json=credentials)
        self.assertEqual(401, resp.status)
