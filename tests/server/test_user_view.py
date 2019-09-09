from aiohttp.test_utils import unittest_run_loop

from tests.server.game_server_test_case import GameServerTestCase

from tests.utils import sync

import tests.mocks.dummy_user_factory as dummies

from engine.server.views.user_view import UserView


class TestUserView(GameServerTestCase):

    @sync
    async def test_get_json_list_of_users(self):
        response = await self.client.get(UserView.__route__)
        json_response = await response.json()
        self.assertEqual(response.status, 200)
        self.assertIsNotNone(json_response)
        self.assertIsInstance(json_response, list)

    @sync
    async def test_put_user_from_json(self):
        dummy_data = dummies.create().__dict__

        response = await self.client.put(
            UserView.__route__,
            json=dummy_data
        )

        self.assertEqual(response.status, 200)

        json_response = await response.json()
        self.assertIsNotNone(json_response)
        self.assertIn('inserted_id', json_response)

