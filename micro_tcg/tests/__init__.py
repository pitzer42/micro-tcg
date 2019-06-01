import asyncio
from micro_tcg import routes
from micro_tcg.server import create_app
from aiohttp.test_utils import AioHTTPTestCase
from micro_tcg.tests.mock_db import (
    create_test_db,
    default_user_data
)


def sync(f):
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        future = f(*args, **kwargs)
        return loop.run_until_complete(future)
    return wrapper


class MicroTcgHttpTestCase(AioHTTPTestCase):

    async def get_application(self):
        test_db = await create_test_db()
        return create_app(db=test_db)

    class LoginResponse:

        def __init__(self):
            self.status = None
            self.json = None
            self.token = None

    async def _request_login(self, password) -> LoginResponse:
        credentials = dict(
            username=default_user_data['username'],
            password=password
        )

        response = await self.client.get(routes.login, json=credentials)
        json_response = await response.json()
        token = json_response['token'] if 'token' in json_response else None

        login = MicroTcgHttpTestCase.LoginResponse()
        login.status = response.status
        login.json = json_response
        login.token = token
        return login

    async def request_successful_login(self) -> LoginResponse:
        password = default_user_data['password']
        return await self._request_login(password)

    async def request_unsuccessful_login(self) -> LoginResponse:
        password = default_user_data['password'] + 'wrong'
        return await self._request_login(password)