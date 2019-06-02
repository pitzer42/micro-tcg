import asyncio
from aiohttp import ClientSession
from micro_tcg import routes


class MicroTCGClient:

    def __init__(self, client, username='user1', base_url= ''):
        self.base_url = base_url
        self.client = client
        self.credentials = dict(
            username=username,
            email=username+'@aiohttp.com',
            password='123123'
        )
        self.socket = None
        self.opponent = None

    async def start(self):
        try:
            await self.register_user()
            await self.login()
            await self.enter_waiting_list()
            await self.match()
        finally:
            await self.socket.close()
            await self.client.close()

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
        ack_json = await self.socket.receive_json()
        print(ack_json['message'])
        return ack_json

    async def match(self):
        match_json = await self.socket.receive_json()
        self.opponent = match_json['opponent']
        print(match_json)


if __name__ == '__main__':
    print('Micro-TCG')
    username = input('username:')
    if username == '':
        username = 'user1'
    micro_tcg_client = MicroTCGClient(
        ClientSession(),
        username=username,
        base_url='http://localhost:8080'
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(micro_tcg_client.start())
