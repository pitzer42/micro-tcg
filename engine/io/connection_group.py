from engine.io.client_connection import ClientConnection


class ConnectionGroup:

    __size_attr__ = 'size'

    def __init__(self, *args):
        self.clients = list()
        if len(args) == 1:
            for client in args[0]:
                self.add(client)

    def add(self, item: ClientConnection):
        item.group = self
        self.clients.append(item)

    def __iter__(self):
        return iter(self.clients)

    def __contains__(self, item):
        if isinstance(item, ClientConnection):
            return item in self.clients
        return False

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

    def but(self, one):
        others = list(self.clients)
        others.remove(one)
        return others
