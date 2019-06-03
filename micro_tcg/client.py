import asyncio
from aiohttp import ClientSession
from micro_tcg import routes


class MicroTCGClient:

    def __init__(self, client, username='user1', base_url=''):
        self.base_url = base_url
        self.client = client
        self.credentials = dict(
            username=username,
            email=username+'@aiohttp.com',
            password='123123'
        )
        self.socket = None
        self.opponent = None

    async def setup(self):
        await self.register_user()
        await self.login()
        await self.enter_waiting_list()
        await self.receive_opponents()

    async def register_user(self):
        return await self.client.put(
            self.base_url + routes.users,
            json=self.credentials
        )

    async def login(self):
        response = await self.client.get(
            self.base_url + routes.login,
            json=self.credentials
        )
        response_json = await response.json()
        self.credentials['token'] = response_json['token']
        return response

    async def enter_waiting_list(self):
        self.socket = await self.client.ws_connect(self.base_url + routes.waiting_list)
        await self.socket.send_json(self.credentials)
        await self.print_message_from_server()

    async def receive_opponents(self):
        opponents_package = await self.print_message_from_server()
        self.opponent = opponents_package['message']

    async def print_and_prompt(self):
        while True:
            await self.prompt_message_to_server()
            await asyncio.sleep(0.5)
            await self.print_message_from_server()

    async def print_message_from_server(self):
        received_message = await self.socket.receive_json()
        print(received_message)
        return received_message

    async def prompt_message_to_server(self):
        sent_message = input(':')
        message_package = dict(
            message=sent_message
        )
        await self.socket.send_json(message_package)
        return sent_message


if __name__ == '__main__':

    async def async_main():
        print('Micro-TCG')

        username = input('username:')
        if username == '':
            username = 'user1'

        micro_tcg_client = MicroTCGClient(
            ClientSession(),
            username=username,
            base_url='http://localhost:8080'
        )

        await micro_tcg_client.setup()
        await micro_tcg_client.print_and_prompt()

    asyncio.run(async_main())
