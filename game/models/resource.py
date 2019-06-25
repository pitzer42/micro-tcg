class Resource(object):

    __slots__ = 'u', 'b', 'r', 'g', 'w'

    def __init__(self, **kwargs):
        for slot in Resource.__slots__:
            value = kwargs.get(slot, 0)
            super(Resource, self).__setattr__(slot, value)

    def __setattr__(self, key, value):
        raise AttributeError('Resource is immutable. Cannot assign ' + str(key))

    def enough(self, cost):
        for res_type in Resource.__slots__:
            owned = getattr(self, res_type)
            required = getattr(cost, res_type)
            if owned < required:
                return False
        return True

    def sum(self, other):
        return self._combine(
            other,
            lambda a, b: a+b
        )

    def sub(self, other):
        return self._combine(
            other,
            lambda a, b: a-b
        )

    def _combine(self, other, operation):
        combined = dict()
        for res_type in Resource.__slots__:
            a = getattr(self, res_type)
            b = getattr(other, res_type)
            combined[res_type] = operation(a, b)
        return Resource(**combined)