from unittest import TestCase

from aiohttp.client import ClientSession

import asyncio

from aiohttp.test_utils import (
    TestServer,
    TestClient,
    AioHTTPTestCase
)

from engine.server import create_game_app

from tests.utils import sync


class GameServerTestCase(AioHTTPTestCase):

    async def get_application(self):
        return create_game_app()
