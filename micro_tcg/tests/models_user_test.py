import unittest

from micro_tcg.models import User
from micro_tcg.tests.mock_db import create_test_db
import asyncio
import json

username = 'tester123'
password = 'password123'
wrong_password = 'password1234'


def sync(f):
    return asyncio.get_event_loop().run_until_complete(f)


class ModelsUserTest(unittest.TestCase):

    def test_encrypt_password_explicitly(self):
        user = User(password=password)
        user.encrypt_password()
        assert user.password != password
        assert user.check_password(password)
        assert not user.check_password(wrong_password)


    def test_passwords_are_encrypted_in_database(self):
        user = User(password=password)
        db = sync(create_test_db())
        sync(user.save(db))
        saved_user = sync(User.get_by_id(db, user._id))
        assert saved_user.password != password
        assert saved_user.check_password(password)
        assert not saved_user.check_password(wrong_password)


    def test_auth(self):
        user = User(
            username=username,
            password=password
        )
        db = sync(create_test_db())
        sync(user.save(db))
        auth_user = sync(User.auth_or_none(db, username, password))
        assert auth_user is not None
        assert auth_user._id == user._id
        assert auth_user.token is not None
