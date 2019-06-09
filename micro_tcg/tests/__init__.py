import asyncio

from aiohttp.test_utils import AioHTTPTestCase

from micro_tcg.server import create_app
from micro_tcg.tests.mocks.mock_db import create_test_db
from micro_tcg.tests.mocks.mock_client import MicroTCGClient


def run_async(f):
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        future = f(*args, **kwargs)
        return loop.run_until_complete(future)
    return wrapper


class MicroTcgApiTestCase(AioHTTPTestCase):

    async def get_application(self):
        """ create application with test database """
        test_db = await create_test_db()
        app = create_app(db=test_db)
        return app

    async def setUpAsync(self) -> None:
        self.use_case = MicroTCGClient(self.client)
        await self.use_case.register_user()