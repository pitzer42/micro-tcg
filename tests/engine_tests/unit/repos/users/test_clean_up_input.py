import unittest

from tests.engine_tests.unit.repos.users import (
    user_data,
    user_data_without_id
)

from engine.models.user import User
from engine.repos.users import clean_up_input


class TestCleanUpInput(unittest.TestCase):

    def test_returns_a_dict(self):
        clean_data = clean_up_input(user_data)
        self.assertIsNotNone(clean_data)
        self.assertIsInstance(clean_data, dict)

    def test_does_not_change_input_parameter(self):
        copy = dict(user_data)
        clean_up_input(copy)
        self.assertEqual(user_data, copy)

    def test_removes_none_id(self):
        clean_data = clean_up_input(user_data_without_id)
        self.assertNotIn(User._id_attr, clean_data)

    def test_preserves_not_none_id(self):
        clean_data = clean_up_input(user_data)
        self.assertIn(User._id_attr, clean_data)

    def test_encrypt_password(self):
        clean_data = clean_up_input(user_data)
        password = clean_data[User._password_attr]
        self.assertIsInstance(password, bytes)
