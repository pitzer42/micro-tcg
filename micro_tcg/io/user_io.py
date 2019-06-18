class ClientConnection:

    def __init__(self, _id, socket):
        self._id = _id
        self.socket = socket
        self._disconnection_message = '%s is disconnected' % str(self._id)

    @property
    def is_connected(self):
        return self.socket.closed

    async def send(self, message):
        if self.socket.closed:
            raise IOError(self._disconnection_message)
        return await self.socket.send_json(message)

    async def receive(self):
        if self.socket.closed:
            raise IOError(self._disconnection_message)
        return await self.socket.receive_json()

    def __eq__(self, other):
        if hasattr(other, '_id'):
            return self._id == getattr(other, '_id')
        if hasattr(other, 'socket'):
            return self.socket == getattr(other, 'socket')
        return False


class ConnectionGroup:

    def __init__(self, clients):
        self.clients = clients

    async def broadcast(self, message):
        for client in self.clients:
            await client.send(message)

    async def multicast(self, emitter, message):
        for client in self.clients:
            if client is not emitter:
                await client.send(message)

    def get_connected_players(self):
        return list(
            filter(
                lambda client: client.is_connected,
                self.clients
            )
        )