import unittest

from tests import run_async
from tests.engine_tests.mocks.db import create_test_db

import engine.storage.user_repo as users

from engine.models.user import User
from engine.crypt import equals_to_encrypted


class TestRepositoryConstraints(unittest.TestCase):

    @run_async
    async def test_passwords_are_encrypted_in_database(self):
        db = await create_test_db()

        clean_password = 'plain_text'
        wrong_password = 'this_is_the_wrong_password'
        user_data = {
            User.__password_attr__: clean_password
        }

        inserted_id = await users.insert(db, user_data)
        saved_user = await users.get_by_id(db, inserted_id)
        hashed_password = saved_user[User.__password_attr__]

        expected_true = equals_to_encrypted(clean_password, hashed_password)
        expected_false = equals_to_encrypted(wrong_password, hashed_password)

        self.assertNotEqual(hashed_password, clean_password)
        self.assertTrue(expected_true)
        self.assertFalse(expected_false)