import unittest

from tests import run_async
from tests.mocks.mock_db import create_test_db

from micro_tcg.crypt import equals_to_encrypted

from micro_tcg.models.user import User

from micro_tcg.storage.user_repo import (
    insert,
    get_by_id,
)


class TestRepositoryConstraints(unittest.TestCase):

    @run_async
    async def test_passwords_are_encrypted_in_database(self):
        db = await create_test_db()

        clean_password = 'plain_text'
        wrong_password = 'this_is_the_wrong_password'
        user_data = {
            User.__password_attr__: clean_password
        }

        inserted_id = await insert(db, user_data)
        saved_user = await get_by_id(db, inserted_id)
        hashed_password = saved_user[User.__password_attr__]

        self.assertNotEqual(hashed_password, clean_password)
        self.assertTrue(equals_to_encrypted(clean_password, hashed_password))
        self.assertFalse(equals_to_encrypted(wrong_password, hashed_password))