import asyncio

import unittest

from aiohttp.test_utils import AioHTTPTestCase
from aiohttp.test_utils import unittest_run_loop

from engine.server import create_game_server

from tests.engine_tests.mocks.db import create_test_db
from tests.engine_tests.mocks.game.client import ChatClient
from tests.engine_tests.mocks.game.game_loop import chat_loop


class ChatTestCase(AioHTTPTestCase):

    async def get_application(self):
        return create_game_server(
            db=await create_test_db(),
            game_loop=chat_loop
        )

    @unittest_run_loop
    async def test_loop(self):
        await self.run_multi_client_test(2)

    @unittest_run_loop
    async def test_simultaneous_loops(self):
        await self.run_multi_client_test(10)

    @unittest.skip
    @unittest_run_loop
    async def test_simultaneous_loops_stress(self):
        await self.run_multi_client_test(200)

    async def run_multi_client_test(self, workload):
        mocks = self.create_mock_clients(workload)
        await ChatTestCase.run_mock_clients(mocks)
        self.assert_mocks_were_grouped_into_pairs(mocks)

    def create_mock_clients(self, n_clients):
        clients = dict()
        for i in range(n_clients):
            client: ChatTestCase = ChatClient(self.client)
            client.user.name = str(i)
            clients[client.user.name] = client
        return clients

    @staticmethod
    async def run_mock_clients(mocks: dict):
        return await asyncio.gather(
            *[m.join_match() for m in mocks.values()]
        )

    def assert_mocks_were_grouped_into_pairs(self, mocks: dict):
        for mock in mocks.values():
            other_key = mock.other_clients_in_chat
            mock_other: ChatTestCase = mocks[other_key]
            self.assertEquals(mock_other.other_clients_in_chat, mock.user.name)
