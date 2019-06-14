def assign_dict_to_obj(obj, **kwargs):
    for key in obj.__dict__.keys():
        if key in kwargs:
            value = kwargs[key]
            setattr(obj, key, value)


class User:

    def __init__(self, **kwargs):
        self.username: str = None
        self.email: str = None
        self.password: str = None
        self.token = None
        assign_dict_to_obj(self, **kwargs)


class Match:

    def __init__(self, **kwargs):
        self.players = list()
        assign_dict_to_obj(self, **kwargs)

    async def game_loop(self):
        pass


class Player:

    def __init__(self, **kwargs):
        self.name: str = None
        self.hand: list[Card] = None
        self.deck: list[Card] = None
        self.field: list[Card] = None
        self.graveyard: list[Card] = None
        self.resources: Resource = None
        assign_dict_to_obj(self, **kwargs)


class Card:

    def __init__(self, **kwargs):
        self.name: str = None
        self.attack: int = 0
        self.defense: int = 0
        self.cost: Resource = None
        assign_dict_to_obj(self, **kwargs)


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
        return self._combine(other, lambda a, b: a+b)

    def sub(self, other):
        return self._combine(other, lambda a, b: a-b)

    def _combine(self, other, operation):
        combined = dict()
        for res_type in Resource.__slots__:
            a = getattr(self, res_type)
            b = getattr(other, res_type)
            combined[res_type] = operation(a, b)
        return Resource(**combined)

