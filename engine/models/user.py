from engine.models import assign_dict_to_obj


class User:

    def __init__(self, **kwargs):
        self.uid = None
        self.name = None
        self.token = None
        self.password = None
        assign_dict_to_obj(self, **kwargs)
