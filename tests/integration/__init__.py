from tests.mocks.mock_db import create_test_db
from tests.mocks.mock_client import MicroTCGClient

from aiohttp.test_utils import AioHTTPTestCase

from micro_tcg.server import create_aiohttp_app


class MicroTcgApiTestCase(AioHTTPTestCase):

    async def get_application(self):
        """ create application with test database """
        test_db = await create_test_db()
        app = create_aiohttp_app(db=test_db)
        return app

    async def setUpAsync(self) -> None:
        self.use_case = MicroTCGClient(self.client)
        await self.use_case.register_user()