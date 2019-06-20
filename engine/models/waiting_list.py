import asyncio
from engine.io.client_connection import ClientConnection
from engine.io.connection_group import ConnectionGroup


class WaitingList:

    def __init__(self, limit: int):
        self.limit: int = limit
        self.w_list: list = list()
        self.ready: asyncio.Event = asyncio.Event()
        self.connection_group: ConnectionGroup = None

    async def next_group(self, client: ClientConnection):
        self.w_list.append(client)
        client_total = len(self.w_list)
        if client_total < self.limit:
            await self.ready.wait()
        else:
            copy = list(self.w_list)
            self.w_list.clear()
            self.connection_group = ConnectionGroup(copy)
            self.ready.set()
            self.ready.clear()
        return self.connection_group
