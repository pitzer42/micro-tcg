class ConnectionGroup:

    __size_attr__ = 'size'

    def __init__(self, clients):
        self.clients = clients

    def __iter__(self):
        return iter(self.clients)

    @property
    def size(self):
        return len(self.clients)

    async def broadcast(self, message):
        for client in self.clients:
            await client.send(message)

    async def multicast(self, emitter, message):
        for client in self.clients:
            if client is not emitter:
                await client.send(message)

    def get_connected_clients(self):
        return list(
            filter(
                lambda client: client.is_connected,
                self.clients
            )
        )
