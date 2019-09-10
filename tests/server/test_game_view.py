from tests.server.game_server_test_case import GameServerTestCase

# from tests.utils import sync
from aiohttp.test_utils import unittest_run_loop as sync

from engine.server.views.game_view import GameView


class TestGameView(GameServerTestCase):

    @sync
    async def test_get_json_ack(self):
        ws = await self.client.ws_connect(GameView.__route__)
        json_response = await ws.receive_json()
        self.assertIn('message', json_response)
        await ws.close()

    @sync
    async def test_get_json_ack_2(self):
        connections = list()
        for _ in range(2):
            ws = await self.client.ws_connect(GameView.__route__)
            connections.append(ws)
            json_response = await ws.receive_json()
            self.assertIn('message', json_response)

        for ws in connections:
            json_response = await ws.receive_json()
            self.assertIn('message', json_response)
            self.assertIn(json_response['message'], 'game on')

        for ws in connections:
            await ws.close()

