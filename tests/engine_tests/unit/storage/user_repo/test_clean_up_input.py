import unittest

from tests.engine_tests.unit.storage.user_repo import (
    user_data,
    user_data_without_id
)

from engine.models.user import User
import engine.storage.user_repo as users


class TestCleanUpInput(unittest.TestCase):

    def test_returns_a_dict(self):
        clean_data = users.clean_up_input(user_data)
        self.assertIsNotNone(clean_data)
        self.assertIsInstance(clean_data, dict)

    def test_does_not_change_input_parameter(self):
        copy = dict(user_data)
        users.clean_up_input(copy)
        self.assertEqual(user_data, copy)

    def test_removes_none_id(self):
        clean_data = users.clean_up_input(user_data_without_id)
        self.assertNotIn(User.__id_attr__, clean_data)

    def test_preserves_not_none_id(self):
        clean_data = users.clean_up_input(user_data)
        self.assertIn(User.__id_attr__, clean_data)

    def test_encrypt_password(self):
        clean_data = users.clean_up_input(user_data)
        password = clean_data[User.__password_attr__]
        self.assertIsInstance(password, bytes)
