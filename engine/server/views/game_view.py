from aiohttp import web

from aiohttp_cors import CorsViewMixin

from engine.client.ws_player import WebSocketPlayer
from engine.models.remote_party import PartyFactory

from  engine.server import app_schema


class GameView(web.View, CorsViewMixin):

    __route__ = '/play'

    @property
    def party_factory(self) -> PartyFactory:
        return self.request.app[app_schema.party_factory]

    @property
    def game_loop(self) -> PartyFactory:
        return self.request.app[app_schema.game_loop]

    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        player = WebSocketPlayer(ws)
        ack = dict(
            message='waiting for other players to join the party.'
        )
        await player.send(ack)
        party = await self.party_factory.gather(player)

        await self.game_loop(player, party)



