import unittest
from engine.models import assign_dict_to_obj


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


class TestAssignDictToObj(unittest.TestCase):
    """ Unit engine_tests for engine_tests.models.assign_dict_to_obj """

    def test_assign_object_s_attributes_using_kwargs(self):
        obj = BaseExampleObject()
        assign_dict_to_obj(obj, **dict_example)
        self.assertEqual(obj.a, dict_example['a'])
        self.assertEqual(obj.b, dict_example['b'])

    def test_assign_sub_object_s_attributes_using_kwargs(self):
        obj = SubExampleObject()
        assign_dict_to_obj(obj, **dict_example_2)
        self.assertEqual(obj.a, dict_example_2['a'])
        self.assertEqual(obj.b, dict_example_2['b'])
        self.assertEqual(obj.c, dict_example_2['c'])
        self.assertEqual(obj.d, dict_example_2['d'])

    def test_assign_only_attrs_that_are_both_in_class_definition_and_in_kwargs(self):
        obj = BaseExampleObject()
        assign_dict_to_obj(obj, **dict_example_2)
        self.assertEqual(obj.a, dict_example_2['a'])
        self.assertEqual(obj.b, dict_example_2['b'])
        self.assertRaises(AttributeError, lambda o: o.c, obj)
        self.assertRaises(AttributeError, lambda o: o.d, obj)
