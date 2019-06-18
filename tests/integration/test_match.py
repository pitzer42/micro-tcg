import asyncio

from aiohttp.test_utils import unittest_run_loop

from tests.integration import MicroTcgApiTestCase
from tests.mocks.mock_client import MicroTCGClient


class TestMatch(MicroTcgApiTestCase):

    @unittest_run_loop
    async def test_match(self):
        client_a = MicroTCGClient(self.client)
        client_b = MicroTCGClient(self.client)
        client_a.user.name = 'user_a'
        client_b.user.name = 'user_b'
        await asyncio.gather(
            client_a.setup(),
            client_b.setup()
        )
        self.assertEqual(client_a.opponent, client_b.user.name)
        self.assertEqual(client_b.opponent, client_a.user.name)


