import bcrypt


def encrypt(value):
    encoded = str(value).encode()
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encoded, salt)


def equals_to_encrypted(value, encrypted_value):
    value = str(value).encode()
    return bcrypt.checkpw(value, encrypted_value)


class Entity:

    def __init__(self, *args, **kwargs):
        def get_value_or_default(dictionary, key, default_value=None):
            return dictionary[key] if key in dictionary else default_value
        for attr in self.__class__.__attributes__:
            value = get_value_or_default(kwargs, attr)
            setattr(self, attr, value)

    @classmethod
    def get_collection(cls, db):
        return db[cls.__collection_name__]

    def as_document(self):
        return self.__dict__

    async def save(self, db):
        collection = self.__class__.get_collection(db)
        doc = self.as_document()
        result = await collection.insert_one(doc)
        return result.inserted_id


class User(Entity):

    __collection_name__ = 'users'
    __attributes__ = (
        'username',
        'email',
        'password',
        'token'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._password = None
        if 'password' in kwargs:
            self.password = kwargs['password']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = encrypt(value)

    @password.deleter
    def password(self):
        del self._password

    @classmethod
    async def auth_or_none(cls, db, username, password):
        collection = cls.get_collection(db)
        query = dict(username=username)
        user_data = await collection.find_one(query)
        if user_data is None:
            return None
        user = User(**user_data)
        if user.check_password(password):
            user.token = encrypt(user_data['_id'])
            query = dict(_id=user_data['_id'])
            await collection.update_one(query, user)
            return user
        return None

    def check_password(self, value):
        return equals_to_encrypted(value, self.password)
