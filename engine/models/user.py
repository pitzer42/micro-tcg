from engine.models import assign_dict_to_obj


class User:

    _id_attr = '_id'
    _name_attr = 'name'
    _token_attr = 'token'
    _password_attr = 'password'

    def __init__(self, **kwargs):
        setattr(self, User._id_attr, None)
        setattr(self, User._name_attr, None)
        setattr(self, User._password_attr, None)
        setattr(self, User._token_attr, None)
        assign_dict_to_obj(self, **kwargs)
