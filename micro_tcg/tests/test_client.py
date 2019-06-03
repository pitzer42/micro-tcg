from aiohttp.test_utils import unittest_run_loop
from micro_tcg.tests import MicroTcgHttpTestCase
from micro_tcg.client import MicroTCGClient
import asyncio


class TestMicroTCGClient(MicroTcgHttpTestCase):

    @unittest_run_loop
    async def test_match(self):
        username_a = 'client_a'
        username_b = 'client_b'
        client_a = MicroTCGClient(self.client, username=username_a)
        client_b = MicroTCGClient(self.client, username=username_b)
        await asyncio.gather(
            client_a.setup(),
            client_b.setup()
        )
        self.assertEqual(client_a.opponent, username_b)
        self.assertEqual(client_b.opponent, username_a)


