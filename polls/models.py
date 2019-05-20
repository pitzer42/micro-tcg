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
        'password'
    )

    def as_document(self):
        doc = self.__dict__
        doc['password'] = encrypt(doc['password'])
        return doc

    def check_password(self, value):
        return equals_to_encrypted(value, self.password)
