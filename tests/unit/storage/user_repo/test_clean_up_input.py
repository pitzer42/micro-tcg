import unittest
from micro_tcg.storage.user_repo import clean_up_input

user_data = dict(
    _id='123',
    name='tester',
    token='some_token',
    password='secret_password'
)

user_data_with_none_id = dict(
    _id=None,
    name='tester',
    token='some_token',
    password='secret_password'
)


class TestCleanUpInput(unittest.TestCase):

    def test_returns_a_dict(self):
        clean_data = clean_up_input(user_data)
        self.assertIsNotNone(clean_data)
        self.assertIsInstance(clean_data, dict)

    def test_does_not_change_input_parameter(self):
        copy = dict(user_data)
        clean_up_input(copy)
        self.assertEqual(user_data, copy)

    def test_removes_id_if_it_is_none(self):
        clean_data = clean_up_input(user_data_with_none_id)
        self.assertNotIn('_id', clean_data)

    def test_preserves_id_if_it_is_not_none(self):
        clean_data = clean_up_input(user_data)
        self.assertIn('_id', clean_data)

    def test_encrypt_password(self):
        clean_data = clean_up_input(user_data)
        password = clean_data['password']
        self.assertIsInstance(password, bytes)
