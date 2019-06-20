import unittest
from tests.engine_tests import run_async
from tests.engine_tests.mocks.mock_db import create_test_db
from engine.storage.user_repo import insert

user_data = dict(
    _id=None,
    name='tester',
    token='some_token',
    password='secret_password'
)


class TestUserRepo(unittest.TestCase):

    _db = None

    @run_async
    async def setUp(self) -> None:
        TestUserRepo._db = await create_test_db()
        inserted_id = await insert(TestUserRepo._db, user_data)
        user_data['_id'] = inserted_id
