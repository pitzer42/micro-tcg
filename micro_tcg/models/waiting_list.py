import asyncio
from micro_tcg.models.match import Match
from micro_tcg.io.client_connection import ClientConnection
from micro_tcg.io.connection_group import ConnectionGroup


# TODO: Move to models and make WaitingList.match a readonly property
# TODO: Make independent of socket
class WaitingList:

    def __init__(self, limit):
        self.limit = limit
        self.next_match: asyncio.Event = None
        self.match: Match = None
        self.waiting = list()

    def add(self, client: ClientConnection):
        self.waiting.append(client)
        if len(self.waiting) == 1:
            self._reset()
        elif len(self.waiting) == self.limit:
            self._create_next_match()

    def _reset(self):
        self.next_match = asyncio.Event()

    def _create_next_match(self):
        match_players = list(self.waiting)
        for player in match_players:
            if player.socket.closed:
                self.waiting.remove(player)
        if len(match_players) != len(self.waiting):
            return
        self.waiting.clear()
        client_group = ConnectionGroup(match_players)
        self.match = Match(clients=client_group)
        self.next_match.set()
