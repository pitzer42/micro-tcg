from tests.engine_tests.mocks.db import create_test_db
from tests.engine_tests.mocks.client import EngineClient

from aiohttp.test_utils import AioHTTPTestCase

from engine.server import create_game_server


class EngineAPITestCase(AioHTTPTestCase):

    async def get_application(self):
        return create_game_server(
            db=await create_test_db()
        )

    async def setUpAsync(self) -> None:
        self.use_case = EngineClient(self.client)
        await self.use_case.register_user()
