from unittest import TestCase

from engine.models.user import User

import tests.mocks.dummy_user_factory as dummies


class TestUser(TestCase):

    def test_create_user_with_default_values(self):
        user = User()
        self.assertEqual(user.name, None)
        self.assertEqual(user.password, None)

    def test_create_user_passing_attributes_by_kwargs(self):
        kwargs = dummies.create().__dict__
        user = User(**kwargs)
        self.assertEqual(user.name, kwargs['name'])
        self.assertEqual(user.password, kwargs['password'])

    def test_create_user_passing_wrong_attributes_by_kwargs(self):
        self.assertRaises(
            TypeError,
            lambda: User(wrong_param=True).wrong_param
        )
