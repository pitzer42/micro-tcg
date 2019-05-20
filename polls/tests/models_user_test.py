import unittest

from polls.models import User


class ModelsUserTest(unittest.TestCase):

    def test_encrypt_password(self):
        default_args = dict(
            username='test_user',
            email='test_user@aiohtttp.com',
            password='password123',
            wrong_password='password1234'
        )
        user = User(**default_args)
        user._encrypt_password()
        self.assertNotEqual(user.password, default_args['password'])
        self.assertFalse(user.check_password(default_args['wrong_password']))
        self.assertTrue(user.check_password(default_args['password']))
