import asyncio

from aiohttp import ClientSession

from tests.engine_tests.mocks.client import EngineClient


class ChatClient(EngineClient):

    def __init__(self, session: ClientSession):
        EngineClient.__init__(self, session)
        self.other_clients_in_chat: str = None

    async def join_match(self):
        await EngineClient.join_match(self)
        await self.introductions()

    async def introductions(self):
        other_clients_in_chat = await self.receive_and_print()
        self.other_clients_in_chat = other_clients_in_chat
        return other_clients_in_chat


if __name__ == '__main__':

    async def client_cli():
        print('Chat')

        client = ChatClient(
            ClientSession()
        )

        client.base_url = 'http://localhost:8080'

        name = input('name:')
        if name != '':
            client.user.name = name

        await client.join_match()
        await client.receive_and_send_loop()

    asyncio.run(client_cli())
