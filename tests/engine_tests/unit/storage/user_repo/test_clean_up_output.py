import unittest

from tests.engine_tests.unit.storage.user_repo import user_data

from engine.models.user import User
import engine.storage.user_repo as users


class TestCleanUpOutput(unittest.TestCase):

    def test_returns_a_dict(self):
        clean_data = users.clean_up_output(user_data)
        self.assertIsNotNone(clean_data)
        self.assertIsInstance(clean_data, dict)

    def test_does_not_change_input_parameter(self):
        copy = dict(user_data)
        users.clean_up_output(copy)
        self.assertEqual(user_data, copy)

    def test_removes_id(self):
        clean_data = users.clean_up_output(user_data)
        self.assertNotIn(User.__id_attr__, clean_data)

    def test_removes_password(self):
        clean_data = users.clean_up_output(user_data)
        self.assertNotIn(User.__password_attr__, clean_data)

    def test_token_is_string(self):
        clean_data = users.clean_up_output(user_data)
        token = clean_data[User.__token_attr__]
        self.assertIsInstance(token, str)

