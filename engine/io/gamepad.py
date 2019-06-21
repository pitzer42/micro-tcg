import asyncio

from aiohttp import ClientSession

from engine import routes
from engine.models.user import User


class Gamepad:

    def __init__(
            self,
            session: ClientSession = None,
            base_url='',
            user: User = None):

        def generate_user() -> User:
            return User(**{
                User.__name_attr__: str(id(self)),
                User.__password_attr__: str(id(self)),
            })

        self.session: ClientSession = session
        self.base_url: str = base_url
        self.socket = None
        self.user: User = generate_user() if user is None else user

    async def start(self):
        await self.register_user()
        await self.login()
        await self.enter_waiting_list()

    async def register_user(self):
        url = self.base_url + routes.users
        doc = self.user.__dict__
        return await self.session.put(
            url,
            json=doc
        )

    async def login(self):
        url = self.base_url + routes.login
        doc = self.user.__dict__
        response = await self.session.get(
            url,
            json=doc
        )
        response_json = await response.json()
        self.user.token = response_json[User.__token_attr__]
        return response

    async def enter_waiting_list(self):
        url = self.base_url + routes.waiting_list
        self.socket = await self.session.ws_connect(url)
        doc = dict(
            token=self.user.token
        )
        await self.socket.send_json(doc)
        return await self.receive_and_print()

    async def get_all_users(self):
        url = self.base_url + routes.users
        return await self.session.get(url)

    async def receive_and_send_loop(self):
        while True:
            await self.prompt_and_send()
            await asyncio.sleep(0.5)
            await self.receive_and_print()

    async def receive_loop(self):
        while True:
            await asyncio.sleep(0.5)
            await self.receive_and_print()

    async def send_loop(self):
        while True:
            await asyncio.sleep(0.5)
            await self.prompt_and_send()

    async def prompt_and_send(self):
        display = self.user.name + '>'
        message = input(display)
        package = dict(
            message=message
        )
        await self.socket.send_json(package)
        return message

    async def receive_and_print(self):
        answer = await self.socket.receive_json()
        display = self.user.name + '<' + repr(answer)
        print(display)
        return answer


if __name__ == '__main__':

    async def connect_gamepad():
        gamepad = Gamepad(
            session=ClientSession()
        )
        gamepad.base_url = 'http://localhost:8080'
        await gamepad.start()
        await gamepad.receive_and_send_loop()

    asyncio.run(connect_gamepad())