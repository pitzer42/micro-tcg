import unittest
from engine.storage.user_repo import clean_up_output

user_data = dict(
    name='tester',
    _id='123',
    token='some_token',
    password='secret_password'
)


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
        self.assertNotIn('_id', clean_data)

    def test_removes_password(self):
        clean_data = clean_up_output(user_data)
        self.assertNotIn('password', clean_data)

    def test_token_is_string(self):
        clean_data = clean_up_output(user_data)
        token = clean_data['token']
        self.assertIsInstance(token, str)

