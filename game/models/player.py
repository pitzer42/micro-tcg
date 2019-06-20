from engine.models import assign_dict_to_obj
from game.models.card import Card
from game.models.resource import Resource


class Player:

    def __init__(self, **kwargs):
        self.name: str = None
        self.hand: list[Card] = None
        self.deck: list[Card] = None
        self.field: list[Card] = None
        self.graveyard: list[Card] = None
        self.resources: Resource = None
        assign_dict_to_obj(self, **kwargs)
