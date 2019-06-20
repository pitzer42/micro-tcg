import asyncio

from aiohttp import ClientSession

from engine import routes
from engine.models.user import User

from tests.engine_tests.unit.storage.user_repo import user_data


class MicroTCGClient:

    def __init__(self, session: ClientSession):
        self.user = User(**user_data)
        self.base_url = ''
        self.session = session
        self.opponent = None
        self.socket = None

    async def setup(self):
        await self.register_user()
        await self.login()
        await self.enter_waiting_list()
        await self.receive_opponents()

    async def get_all_users(self):
        url = self.base_url + routes.users
        return await self.session.get(url)

    async def register_user(self):
        url = self.base_url + routes.users
        doc = self.user.__dict__
        return await self.session.put(
            url,
            json=doc
        )

    async def login(self, expect_success=True):
        url = self.base_url + routes.login
        doc = self.user.__dict__
        response = await self.session.get(
            url,
            json=doc
        )
        if expect_success:
            response_json = await response.json()
            self.user.token = response_json[User.__token_attr__]
        return response

    async def login_with_wrong_name(self):
        bkp = self.user.name
        self.user.name += 'wrong'
        response = await self.login(expect_success=False)
        self.user.name = bkp
        return response

    async def login_with_wrong_password(self):
        bkp = self.user.password
        self.user.password += 'wrong'
        response = await self.login(expect_success=False)
        self.user.password = bkp
        return response

    async def enter_waiting_list(self):
        url = self.base_url + routes.waiting_list
        self.socket = await self.session.ws_connect(url)
        doc = dict(
            token=self.user.token
        )
        await self.socket.send_json(doc)
        return await self.receive_and_print()

    async def receive_opponents(self):
        opponents = await self.receive_and_print()
        self.opponent = opponents['message']
        return opponents

    async def receive_and_send_loop(self):
        while True:
            await self.prompt_and_send()
            await asyncio.sleep(0.5)
            await self.receive_and_print()

    async def prompt_and_send(self):
        message = input(':')
        package = dict(
            message=message
        )
        await self.socket.send_json(package)
        return message

    async def receive_and_print(self):
        answer = await self.socket.receive_json()
        print(answer)
        return answer


if __name__ == '__main__':

    async def client_cli():
        print('Micro-TCG')

        client = MicroTCGClient(
            ClientSession()
        )

        client.base_url = 'http://localhost:8080'

        name = input('name:')
        if name != '':
            client.user.name = name

        await client.setup()
        await client.receive_and_send_loop()

    asyncio.run(client_cli())
