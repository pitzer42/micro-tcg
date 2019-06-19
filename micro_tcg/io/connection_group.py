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

    def get_connected_clients(self):
        return list(
            filter(
                lambda client: client.is_connected,
                self.clients
            )
        )