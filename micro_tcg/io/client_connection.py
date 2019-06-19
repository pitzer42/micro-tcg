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
        if isinstance(other, ClientConnection):
            return self._id == getattr(other, '_id')
        return False
