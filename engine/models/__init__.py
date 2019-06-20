def assign_dict_to_obj(obj, **kwargs):
    for key in obj.__dict__.keys():
        if key in kwargs:
            value = kwargs[key]
            setattr(obj, key, value)