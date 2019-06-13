from micro_tcg.crypto import *


def assign_dict_to_obj(obj, **kwargs):
    for key in obj.__dict__.keys():
        if key in kwargs:
            value = kwargs[key]
            setattr(obj, key, value)


class Entity:

    ID_ATTR = '_id'

    def __init__(self, *args, **kwargs):
        self._id = None
        assign_dict_to_obj(self, **kwargs)

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

        self.username = None
        self.email = None
        self.password = None
        self.token = None

        assign_dict_to_obj(self, **kwargs)

    async def save(self, db):
        bkp = self.password
        self.encrypt_password()
        await Entity.save(self, db)
        self.password = bkp

    def encrypt_password(self):
        self.password = encrypt(self.password)
        return self.password

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

    @classmethod
    async def validate_token(cls, db, token):
        collection = cls.get_collection(db)
        query = dict(token=token)
        user_data = await collection.find_one(query)
        if user_data is None:
            return None
        user = User(**user_data)
        return user

    def check_password(self, value):
        return equals_to_encrypted(value, self.password)
