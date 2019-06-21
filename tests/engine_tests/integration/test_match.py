import asyncio

import unittest

from aiohttp.test_utils import unittest_run_loop

from tests.engine_tests.integration import MicroTcgApiTestCase
from tests.engine_tests.mocks.mock_client import MicroTCGClient


class TestMatch(MicroTcgApiTestCase):

    @unittest_run_loop
    async def test_match(self):
        await self.run_multi_client_test(2)

    @unittest_run_loop
    async def test_simultaneous_matches(self):
        await self.run_multi_client_test(10)

    @unittest.skip
    @unittest_run_loop
    async def test_simultaneous_matches_stress(self):
        await self.run_multi_client_test(200)

    async def run_multi_client_test(self, workload):
        mocks = self.create_mock_clients(workload)
        await TestMatch.run_mock_clients(mocks)
        self.assert_mocks_were_grouped_into_pairs(mocks)

    def create_mock_clients(self, n_clients):
        clients = dict()
        for i in range(n_clients):
            client = MicroTCGClient(self.client)
            client.user.name = str(i)
            clients[client.user.name] = client
        return clients

    @staticmethod
    async def run_mock_clients(mocks: dict):
        return await asyncio.gather(
            *[m.setup() for m in mocks.values()]
        )

    def assert_mocks_were_grouped_into_pairs(self, mocks: dict):
        for mock in mocks.values():
            opponent_key = mock.opponent
            mock_opponent = mocks[opponent_key]
            self.assertEquals(mock_opponent.opponent, mock.user.name)
