import unittest
from game.models.resource import Resource

expected_resource_types = [
        'u',
        'b',
        'r',
        'g',
        'w'
]


class TestResource(unittest.TestCase):

    def test_resource_has_one_attribute_for_each_type_of_resource(self):
        res_pool = Resource()
        for res_type in expected_resource_types:
            self.assertTrue(hasattr(res_pool, res_type))

    def test_resource_is_immutable(self):
        pool = Resource()

        def change_pool():
            res_type = expected_resource_types[0]
            setattr(pool, res_type, 1)

        self.assertRaises(AttributeError, change_pool)

    def test_enough_resources_to_pay_cost(self):
        res_type = expected_resource_types[0]
        res_pool = Resource(**{
            res_type: 1
        })
        cost = Resource(**{
            res_type: 1
        })
        self.assertTrue(res_pool.enough(cost))

    def test_few_resources_to_pay_cost(self):
        res_type = expected_resource_types[0]
        res_pool = Resource(**{
            res_type: 0
        })
        cost = Resource(**{
            res_type: 1
        })
        self.assertFalse(res_pool.enough(cost))

    def test_a_type_of_resource_is_not_enough_to_pay_for_a_different_type_of_cost(self):
        res_type_a = expected_resource_types[0]
        res_type_b = expected_resource_types[1]
        pool = Resource(**{
            res_type_a: 1
        })
        cost = Resource(**{
            res_type_b: 1
        })
        self.assertFalse(pool.enough(cost))

    def test_sum_resources(self):
        res_type_a = expected_resource_types[0]
        res_type_b = expected_resource_types[1]
        pool_a = Resource(**{
            res_type_a: 1,
            res_type_b: 1
        })
        pool_b = Resource(**{
            res_type_a: 1
        })
        result_pool = pool_a.sum(pool_b)

        a_result = getattr(result_pool, res_type_a)
        b_result = getattr(result_pool, res_type_b)
        expected_a_result = getattr(pool_a, res_type_a) + getattr(pool_b, res_type_a)
        expected_b_result = getattr(pool_a, res_type_b) + getattr(pool_b, res_type_b)

        self.assertEqual(a_result, expected_a_result)
        self.assertEqual(b_result, expected_b_result)

    def test_sub_resources(self):
        res_type_a = expected_resource_types[0]
        res_type_b = expected_resource_types[1]
        pool_a = Resource(**{
            res_type_a: 1,
            res_type_b: 1
        })
        pool_b = Resource(**{
            res_type_a: 1
        })
        result_pool = pool_a.sub(pool_b)

        a_result = getattr(result_pool, res_type_a)
        b_result = getattr(result_pool, res_type_b)
        expected_a_result = getattr(pool_a, res_type_a) - getattr(pool_b, res_type_a)
        expected_b_result = getattr(pool_a, res_type_b) - getattr(pool_b, res_type_b)

        self.assertEqual(a_result, expected_a_result)
        self.assertEqual(b_result, expected_b_result)

