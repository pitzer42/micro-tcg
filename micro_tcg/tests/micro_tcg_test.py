from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from micro_tcg.main import create_app
from micro_tcg.tests.mock_db import create_test_db, user_data


class TestApp(AioHTTPTestCase):

    async def get_application(self):
        test_db = await create_test_db()
        return create_app(db=test_db)

    @unittest_run_loop
    async def test_get_users(self):
        resp = await self.client.request("GET", "/users")
        assert resp.status == 200
        json_response = await resp.json()
        assert json_response
        assert json_response[0]['username'] == user_data['username']

    @unittest_run_loop
    async def test_put_user(self):
        request_data = dict(
            username='test_put_user',
            email='test_put_user@aiohtp.com',
            password='test_put_user_123'
        )
        resp = await self.client.put("/users", json=request_data)
        assert resp.status == 200
        assert await resp.json()

    @unittest_run_loop
    async def test_successful_login(self):
        resp = await self.client.get("/users/login", json=user_data)
        assert resp.status == 200
        json_response = await resp.json()
        assert json_response
        assert 'token' in json_response

    @unittest_run_loop
    async def test_unsuccessful_login(self):
        credentials = dict(user_data)
        credentials['password'] += credentials['password']
        resp = await self.client.get("/users/login", json=credentials)
        json_response = await resp.json()
        assert json_response
        assert 'message' in json_response
        assert 'token' not in json_response
