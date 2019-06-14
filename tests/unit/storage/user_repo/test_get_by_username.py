import unittest

from tests import run_async
from tests.mocks.mock_db import create_test_db

from micro_tcg.storage.user_repo import (
    insert,
    get_by_username
)

user_data = dict(
    _id=None,
    name='tester',
    token='some_token',
    password='secret_password'
)


class TestGetByUsername(unittest.TestCase):

    @run_async
    async def setUp(self) -> None:
        db = await create_test_db()
        inserted_id = await insert(db, user_data)
        user_data['_id'] = inserted_id

    @run_async
    def test_smoke(self):
        self.assertIsNotNone(user_data['_id'])



