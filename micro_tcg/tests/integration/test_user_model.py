import unittest

from micro_tcg.models import User
from micro_tcg.tests import run_async
from micro_tcg.tests.mocks.mock_db import create_test_db

username = 'tester123'
password = 'password123'
wrong_password = 'password1234'


class ModelsUserTest(unittest.TestCase):

    def test_encrypt_password_explicitly(self):
        user = User(password=password)
        user.encrypt_password()
        self.assertNotEqual(user.password, password)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.check_password(wrong_password))

    @run_async
    async def test_passwords_are_encrypted_in_database(self):
        user = User(password=password)
        db = await create_test_db()
        await user.save(db)
        saved_user = await User.get_by_id(db, user._id)
        self.assertNotEqual(saved_user.password, password)
        self.assertTrue(saved_user.check_password(password))
        self.assertFalse(saved_user.check_password(wrong_password))

    @run_async
    async def test_auth(self):
        user = User(
            username=username,
            password=password
        )
        db = await create_test_db()
        await user.save(db)
        auth_user = await User.auth_or_none(db, username, password)
        self.assertIsNotNone(auth_user)
        self.assertEqual(auth_user._id, user._id)
        self.assertIsNotNone(auth_user.token)