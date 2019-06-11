import unittest
from micro_tcg import models

plain_text = 'plaintext'

plain_values = [
    plain_text,
    123,
    1.23,
    dict(),
    list(),
    object,
    b'bytes'
]

dict_example = dict(
    a=1,
    b=2
)

dict_example_2 = dict(
    a=1,
    b=2,
    c=3,
    d=4
)


class BaseExampleObject:

    def __init__(self, *args, **kwargs):
        self.a = None
        self.b = None


class SubExampleObject(BaseExampleObject):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.c = None
        self.d = None


class TestEncrypt(unittest.TestCase):
    """ Unit tests for micro_tcg.models.encrypt """

    def test_hash_is_different_from_plain_text(self):
        hashed = models.encrypt(plain_text)
        self.assertNotEqual(plain_text, hashed)

    def test_hash_type_is_bytes(self):
        hashed = models.encrypt(plain_text)
        self.assertIsInstance(hashed, bytes)

    def test_hashes_any_type(self):
        try:
            map(models.encrypt, plain_values)
        except Exception as e:
            self.fail(msg=str(e))


class TestEqualsToEncrypted(unittest.TestCase):
    """ Unit tests for micro_tcg.models.equals_to_encrypted """

    def test_compares_original_plain_value_to_hashed_value(self):
        hashes = list(map(models.encrypt, plain_values))
        try:
            for i in range(len(hashes)):
                plain_value = plain_values[i]
                hash_value = hashes[i]
                are_equal = models.equals_to_encrypted(plain_value, hash_value)
                self.assertTrue(are_equal)
        except Exception as e:
            self.fail(msg=str(e))


class TestAssignDictToObj(unittest.TestCase):
    """ Unit tests for micro_tcg.models.assign_dict_to_obj """

    def test_assign_object_s_attributes_using_kwargs(self):
        obj = BaseExampleObject()
        models.assign_dict_to_obj(obj, **dict_example)
        self.assertEqual(obj.a, dict_example['a'])
        self.assertEqual(obj.b, dict_example['b'])

    def test_assign_sub_object_s_attributes_using_kwargs(self):
        obj = SubExampleObject()
        models.assign_dict_to_obj(obj, **dict_example_2)
        self.assertEqual(obj.a, dict_example_2['a'])
        self.assertEqual(obj.b, dict_example_2['b'])
        self.assertEqual(obj.c, dict_example_2['c'])
        self.assertEqual(obj.d, dict_example_2['d'])

    def test_assign_only_attrs_that_are_both_in_class_definition_and_in_kwargs(self):
        obj = BaseExampleObject()
        models.assign_dict_to_obj(obj, **dict_example_2)
        self.assertEqual(obj.a, dict_example_2['a'])
        self.assertEqual(obj.b, dict_example_2['b'])
        self.assertRaises(AttributeError, lambda o: o.c, obj)
        self.assertRaises(AttributeError, lambda o: o.d, obj)
