import unittest

from tests.engine_tests.unit.repos.users import (
    user_data
)

from engine.repos.schemas.user import (
    uid_attr,
    token_attr,
    password_attr
)
from engine.repos.users import clean_up_output


class TestCleanUpOutput(unittest.TestCase):

    def test_returns_a_dict(self):
        clean_data = clean_up_output(user_data)
        self.assertIsNotNone(clean_data)
        self.assertIsInstance(clean_data, dict)

    def test_does_not_change_input_parameter(self):
        copy = dict(user_data)
        clean_up_output(copy)
        self.assertEqual(user_data, copy)

    def test_removes_id(self):
        clean_data = clean_up_output(user_data)
        self.assertNotIn(uid_attr, clean_data)

    def test_removes_password(self):
        clean_data = clean_up_output(user_data)
        self.assertNotIn(password_attr, clean_data)

    def test_token_is_string(self):
        clean_data = clean_up_output(user_data)
        token = clean_data[token_attr]
        self.assertIsInstance(token, str)

