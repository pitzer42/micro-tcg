import unittest
from tests import run_async
from tests.mocks.mock_db import create_test_db
from micro_tcg.storage.user_repo import insert

user_data = dict(
    _id=None,
    name='tester',
    token='some_token',
    password='secret_password'
)


class TestUserRepo(unittest.TestCase):

    __db__ = None

    @run_async
    async def setUp(self) -> None:
        TestUserRepo.__db__ = await create_test_db()
        inserted_id = await insert(TestUserRepo.__db__, user_data)
        user_data['_id'] = inserted_id
