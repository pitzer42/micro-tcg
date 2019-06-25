from engine.io.client_connection import ClientConnection


class ConnectionGroup(list):

    def __init__(self, *args):
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            for item in args[0]:
                self.append(item)

    def append(self, item: ClientConnection):
        if not isinstance(item, ClientConnection):
            raise TypeError('ConnectionGroup only accept ClientConnection as members')
        item.group = self
        list.append(self, item)

    @property
    def size(self):
        return len(self)

    async def broadcast(self, message):
        for client in self:
            await client.send(message)

    async def multicast(self, emitter, message):
        for client in self:
            if client is not emitter:
                await client.send(message)

    def get_connected_clients(self):
        return list(
            filter(
                lambda client: client.is_connected,
                self
            )
        )

    def except_for(self, one):
        others = list(self)
        others.remove(one)
        return others
