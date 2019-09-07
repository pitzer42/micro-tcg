from unittest import TestCase

from aiohttp.client import ClientSession

from tests.utils import sync


class GameServerTestCase(TestCase):

    _client: ClientSession = None

    @property
    def client(self) -> ClientSession:
        return GameServerTestCase._client
        GameServerTestCase._client.put()


    @classmethod
    @sync
    async def setUpClass(cls) -> None:
        GameServerTestCase._client = ClientSession()
        original_request_method = GameServerTestCase._client._request

        async def custom_request_method(*args, **kwargs):
            url = 'http://localhost:8080' + args[1]
            custom_args = list(args)
            custom_args[1] = url
            return await original_request_method(*custom_args, **kwargs)

        GameServerTestCase._client._request = custom_request_method


    @classmethod
    @sync
    async def tearDownClass(cls) -> None:
        try:
            await GameServerTestCase._client.close()
        except RuntimeError as e:
            raise e
