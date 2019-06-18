__name_attr__ = 'name'
__token_attr__ = 'token'
__password_attr__ = 'password'

from micro_tcg.models import assign_dict_to_obj


class User:

    __id_attr__ = '_id'
    __name_attr__ = 'name'
    __token_attr__ = 'token'
    __password_attr__ = 'password'

    def __init__(self, **kwargs):
        setattr(self, User.__id_attr__, None)
        setattr(self, User.__name_attr__, None)
        setattr(self, User.__password_attr__, None)
        setattr(self, User.__token_attr__, None)
        assign_dict_to_obj(self, **kwargs)
