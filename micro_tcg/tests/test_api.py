from micro_tcg import routes
from aiohttp.test_utils import unittest_run_loop
from micro_tcg.tests import MicroTcgHttpTestCase


class TestUsersAPI(MicroTcgHttpTestCase):

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


class TestAuthAPI(MicroTcgHttpTestCase):

    @unittest_run_loop
    async def test_successful_login(self):
        response = await self.request_successful_login()
        self.assertEqual(200, response.status)
        self.assertIsNotNone(response.json)
        self.assertIsNotNone(response.token)

    @unittest_run_loop
    async def test_unsuccessful_login(self):
        response = await self.request_unsuccessful_login()
        self.assertIsNotNone(response.json)
        self.assertIn('message', response.json)
        self.assertNotIn('token', response.json)

    @unittest_run_loop
    async def test_successful_access_to_protected_view(self):
        response = await self.request_successful_login()
        response = await self.client.get(routes.secret, json=response.json)
        self.assertEqual(200, response.status)

    @unittest_run_loop
    async def test_unsuccessful_access_to_protected_view(self):
        credentials = dict(
            token='invalid_token'
        )
        response = await self.client.get(
            routes.secret,
            json=credentials
        )
        self.assertEqual(401, response.status)

    @unittest_run_loop
    async def test_entering_waiting_list(self):
        response = await self.request_successful_login()
        async with self.client.ws_connect(routes.waiting_list) as ws:
            self.assertIsNotNone(ws)
            await ws.send_str(response.token)
            ack = await ws.receive_str()
            self.assertIsNotNone(ack)

    @unittest_run_loop
    async def test_entering_waiting_list(self):
        response = await self.request_successful_login()
        async with self.client.ws_connect(routes.waiting_list) as ws:
            self.assertIsNotNone(ws)
            await ws.send_str(response.token)
            ack = await ws.receive_str()
            self.assertIsNotNone(ack)
