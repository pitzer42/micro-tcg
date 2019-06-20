from engine.models import assign_dict_to_obj
from game.resource import Resource


class Card:

    def __init__(self, **kwargs):
        self.name: str = None
        self.attack: int = 0
        self.defense: int = 0
        self.cost: Resource = None
        assign_dict_to_obj(self, **kwargs)
