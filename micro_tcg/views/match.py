from micro_tcg.views.decorators import require_auth_web_socket
import asyncio


class Match:

    def __init__(self, players: list):
        self.players = players
        self.running = False

    async def start(self, player):
        try:
            message_package = self.welcome_message_for(player)
            await player.send(message_package)
            async for package in player.socket:
                message = package.data
                print(player.name + ':' + message)
                await self.multicast(player, package)
        except IOError as error:
            print(error)

    def welcome_message_for(self, player):
        others = self.other_players(player)
        other_names = ''
        for other in others:
            other_names += other.name + ', '
        other_names = other_names[0:-2]
        return dict(message=other_names)

    async def broadcast(self, message):
        for player in self.players:
            await player.send(message)

    async def multicast(self, emitter, message):
        for player in self.other_players(emitter):
            await player.send(message)

    def other_players(self, player):
        other_players = list(self.players)
        other_players.remove(player)
        return other_players

    def get_connected_players(self):
        connected_players = list()
        for player in self.players:
            if not player.socket.closed:
                connected_players.append(player)
        return connected_players


class Player:

    def __init__(self, name, socket):
        self.name = name
        self.socket = socket
        self.match = None
        self._disconnection_message = '%s is disconnected' % str(self.name)

    async def send(self, message):
        if self.socket.closed:
            raise IOError(self._disconnection_message)
        return await self.socket.send_json(message)

    async def receive(self):
        if self.socket.closed:
            raise IOError(self._disconnection_message)
        return await self.socket.receive_json()


class WaitingList:

    def __init__(self, limit):
        self.limit = limit
        self.next_match: asyncio.Event = None
        self.match: Match = None
        self.waiting = list()

    def add(self, player):
        self.waiting.append(player)
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
        self.match = Match(match_players)
        self.next_match.set()


@require_auth_web_socket
async def enter_waiting_list(request, socket, user):
    waiting_list = request.app['waiting_list']

    player = Player(user.username, socket)
    ack = dict(message='you are now in the waiting list')
    await player.send(ack)

    waiting_list.add(player)
    await waiting_list.next_match.wait()
    await waiting_list.match.start(player)

    return socket
