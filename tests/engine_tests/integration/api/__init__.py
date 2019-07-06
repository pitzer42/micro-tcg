
from tests.engine_tests.mocks.client import TestGamepad

from aiohttp.test_utils import AioHTTPTestCase

from engine.server import create_game_server

from tests.engine_tests.mocks.repositories import create_test_repositories


class EngineAPITestCase(AioHTTPTestCase):

    async def get_application(self):
        return create_game_server(
            repositories=await create_test_repositories()
        )

    async def setUpAsync(self) -> None:
        self.use_case = TestGamepad(self.client)
