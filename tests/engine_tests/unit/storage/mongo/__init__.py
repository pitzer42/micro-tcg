import unittest

from tests import run_async
from tests.engine_tests.mocks.repositories import create_test_repositories


class TestRepositories(unittest.TestCase):

    @run_async
    async def setUp(self) -> None:
        self.repositories = await create_test_repositories()
