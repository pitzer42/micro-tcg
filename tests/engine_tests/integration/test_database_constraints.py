from tests import run_async

from tests.engine_tests.unit.storage.mongo.users import TestUsers

from engine.models.user import User
from engine.crypt import equals_to_encrypted


class TestRepositoryConstraints(TestUsers):

    @run_async
    async def test_passwords_are_encrypted_in_database(self):
        clean_password = 'plain_text'
        wrong_password = 'this_is_the_wrong_password'
        user_data = {
            User._password_attr: clean_password
        }

        inserted_id = await self.users.insert(user_data)
        saved_user = await self.users.get_by_id(inserted_id)
        hashed_password = saved_user[User._password_attr]

        expected_true = equals_to_encrypted(clean_password, hashed_password)
        expected_false = equals_to_encrypted(wrong_password, hashed_password)

        self.assertNotEqual(hashed_password, clean_password)
        self.assertTrue(expected_true)
        self.assertFalse(expected_false)
