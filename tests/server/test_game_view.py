from tests.server.game_server_test_case import GameServerTestCase

from tests.utils import sync

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
        ws = await self.client.ws_connect(GameView.__route__)
        json_response = await ws.receive_json()
        self.assertIn('message', json_response)
        json_response = await ws.receive_json()
        self.assertIn('message', json_response)
        self.assertEqual(json_response['message'], 'game on')
        await ws.close()
