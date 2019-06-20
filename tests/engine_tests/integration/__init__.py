from tests.engine_tests.mocks.mock_db import create_test_db
from tests.engine_tests.mocks.mock_game_loop import game_loop
from tests.engine_tests.mocks.mock_client import MicroTCGClient

from aiohttp.test_utils import AioHTTPTestCase

from engine.server import create_aiohttp_app


class MicroTcgApiTestCase(AioHTTPTestCase):

    async def get_application(self):
        """ create application with test database """
        return create_aiohttp_app(
            db=await create_test_db(),
            game_loop=game_loop
        )

    async def setUpAsync(self) -> None:
        self.use_case = MicroTCGClient(self.client)
        await self.use_case.register_user()