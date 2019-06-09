import asyncio

from aiohttp.test_utils import unittest_run_loop

from micro_tcg.tests import MicroTcgApiTestCase
from micro_tcg.tests.mocks.mock_client import MicroTCGClient


class TestMatch(MicroTcgApiTestCase):

    @unittest_run_loop
    async def test_match(self):
        client_a = MicroTCGClient(self.client)
        client_b = MicroTCGClient(self.client)
        client_a.user.username = 'user_a'
        client_b.user.username = 'user_b'
        await asyncio.gather(
            client_a.setup(),
            client_b.setup()
        )
        self.assertEqual(client_a.opponent, client_b.user.username)
        self.assertEqual(client_b.opponent, client_a.user.username)


