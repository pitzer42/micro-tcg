import unittest

from tests import run_async
from tests.engine_tests.mocks.db import create_test_db

from engine.models.user import User
import engine.storage.user_repo as users

user_data = {
    User.__id_attr__: '123',
    User.__name_attr__: 'tester',
    User.__token_attr__: 'some_token',
    User.__password_attr__: 'secret_password'
}

user_data_without_id = {
    User.__id_attr__: None,
    User.__name_attr__: 'tester',
    User.__token_attr__: 'some_token',
    User.__password_attr__: 'secret_password'
}


class TestUserRepo(unittest.TestCase):

    db = None

    @run_async
    async def setUp(self) -> None:
        db = await create_test_db()
        inserted_id = await users.insert(db, user_data)
        user_data[User.__id_attr__] = inserted_id
        TestUserRepo.db = db
