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
            if len(copy) != self.limit:
                print('BUG 1')
            self.connection_group = ConnectionGroup(copy)
            print('waiters ' + str(len(self.ready._waiters)))
            self.ready.set()

        if client not in self.connection_group:
            print('BUG 2')

        return self.connection_group
