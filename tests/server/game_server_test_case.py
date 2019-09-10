from aiohttp.test_utils import AioHTTPTestCase

from engine.server import create_game_app

from engine.models.remote_party import RemoteParty
from engine.models.remote_player import RemotePlayer


async def test_game_loop(player: RemotePlayer, party: RemoteParty):
    if player == party[0]:
        await party.broadcast(dict(
            message='game on'
        ))


class GameServerTestCase(AioHTTPTestCase):

    async def get_application(self):
        return create_game_app(
            game_loop=test_game_loop
        )
