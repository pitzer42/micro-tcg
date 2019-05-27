import unittest

from micro_tcg.models import User


password = 'password123',
wrong_password = 'password1234'


class ModelsUserTest(unittest.TestCase):

    def test_encrypts_password_in_constructor(self):
        user = User(password=password)
        assert user.password != password
        assert user.check_password(password)
        assert not user.check_password(wrong_password)


    def test_encrypts_password_in_property_assign(self):
        user = User()
        user.password = password
        assert user.password != password
        assert user.check_password(password)
        assert not user.check_password(wrong_password)
