import asyncio

from engine.io.client_connection import ClientConnection
from engine.io.connection_group import ConnectionGroup


class WaitingList:

    def __init__(self, limit: int):
        self.limit: int = limit
        self.w_list = list()

    async def next_group(self, client: ClientConnection):
        event = asyncio.Event()
        self.w_list.append((
            client,
            event
        ))
        self._create_group()
        await event.wait()
        return client.group

    def _create_group(self):
        if len(self.w_list) >= self.limit:
            group = ConnectionGroup()
            for i in range(self.limit):
                client, event = self.w_list.pop()
                group.add(client)
                event.set()
