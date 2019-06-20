import asyncio

from aiohttp.test_utils import unittest_run_loop

from tests.engine_tests.integration import MicroTcgApiTestCase
from tests.engine_tests.mocks.mock_client import MicroTCGClient


class TestMatch(MicroTcgApiTestCase):

    @staticmethod
    async def run_mock_clients(mocks: dict):
        return await asyncio.gather(
            *[m.setup() for m in mocks.values()]
        )

    def create_mock_clients(self, n_clients):
        clients = dict()
        for i in range(n_clients):
            client = MicroTCGClient(self.client)
            client.user.name = str(i)
            clients[client.user.name] = client
        return clients

    def assert_mocks_were_grouped_into_pairs(self, mocks: dict):
        for mock in mocks.values():
            opponent_key = mock.opponent
            mock_opponent = mocks[opponent_key]
            self.assertEquals(mock_opponent.opponent, mock.user.name)

    @unittest_run_loop
    async def test_match(self):
        mocks = self.create_mock_clients(2)
        await TestMatch.run_mock_clients(mocks)
        self.assert_mocks_were_grouped_into_pairs(mocks)

    @unittest_run_loop
    async def test_simultaneous_matches(self):
        mocks = self.create_mock_clients(10)
        await TestMatch.run_mock_clients(mocks)
        self.assert_mocks_were_grouped_into_pairs(mocks)

