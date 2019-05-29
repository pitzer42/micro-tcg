import bcrypt


def encrypt(value):
    encoded = str(value).encode()
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encoded, salt)


def equals_to_encrypted(value, encrypted_value):
    value = str(value).encode()
    return bcrypt.checkpw(value, encrypted_value)


def get_value_or_default(d: dict, key, default=None):
    return d[key] if key in d else default


def assign_from_dict(obj, d: dict, *attrs):
    for attr in attrs:
        value = get_value_or_default(d, attr)
        setattr(obj, attr, value)


class Entity:

    ID_ATTR = '_id'

    def __init__(self, *args, **kwargs):
        assign_from_dict(self, kwargs, Entity.ID_ATTR)

    @classmethod
    def get_collection(cls, db):
        return db[cls.__collection_name__]

    @classmethod
    async def get_by_id(cls, db, _id):
        collection = cls.get_collection(db)
        query = dict(_id=_id)
        obj_data = await collection.find_one(query)
        return cls(**obj_data)

    def as_document(self):
        return self.__dict__.copy()

    async def save(self, db):
        collection = self.__class__.get_collection(db)
        doc = self.as_document()
        if self._id is None:
            del doc[Entity.ID_ATTR]
        result = await collection.insert_one(doc)
        self._id = result.inserted_id
        return result.inserted_id


class User(Entity):

    __collection_name__ = 'users'

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        assign_from_dict(self, kwargs,
                         'username',
                         'email',
                         'password',
                         'token'
                         )

    def encrypt_password(self):
        self.password = encrypt(self.password)
        return self.password

    def as_document(self):
        doc = super().as_document()
        if not isinstance(doc['password'], bytes):
            doc['password'] = encrypt(doc['password'])
        return doc

    @classmethod
    async def auth_or_none(cls, db, username, password):
        collection = cls.get_collection(db)
        query = dict(username=username)
        user_data = await collection.find_one(query)
        if user_data is None:
            return None
        user = User(**user_data)
        if user.check_password(password):
            user.token = encrypt(user_data[Entity.ID_ATTR])
            query = dict(_id=user_data[Entity.ID_ATTR])
            update_data = {'$set': user.as_document()}
            await collection.update_one(query, update_data)
            return user
        return None

    def check_password(self, value):
        return equals_to_encrypted(value, self.password)
