__storage_name__ = 'users'

from engine.models .user import User
from engine.crypt import encrypt


def get_collection(db):
    return db[__storage_name__]


async def get_by_name(db, name: str):
    collection = get_collection(db)
    query = {
        User.__name_attr__: name
    }
    return await collection.find_one(query)


async def get_by_id(db, user_id: str):
    collection = get_collection(db)
    query = {
        User.__id_attr__: user_id
    }
    return await collection.find_one(query)


async def get_by_token(db, token):
    collection = get_collection(db)
    query = {
        User.__token_attr__: token
    }
    return await collection.find_one(query)


async def count(db, query=dict()):
    collection = get_collection(db)
    return await collection.count_documents(query)


async def list_all(db, limit=100):
    collection = get_collection(db)
    cursor = collection.find()
    users_data = await cursor.to_list(length=limit)
    users = list()
    for user_data in users_data:
        clean_user_data = clean_up_output(user_data)
        users.append(clean_user_data)
    return users


async def insert(db, user_data: dict):
    collection = get_collection(db)
    user_data = clean_up_input(user_data)
    result = await collection.insert_one(user_data)
    return result.inserted_id


async def set_token(db, user_id, token):
    collection = get_collection(db)
    query = {
        User.__id_attr__: user_id
    }
    operation = operation_set(token=token)
    return await collection.update_one(query, operation)


async def replace_token(db, old_token, updated_token):
    collection = get_collection(db)
    query = {
        User.__token_attr__: old_token
    }
    operation = operation_set(token=updated_token)
    return await collection.update_one(query, operation)


# TODO: Adapters?
def clean_up_output(user_data: dict) -> dict:
    clean_data = dict(user_data)
    # remove _id and password from the payload
    del clean_data[User.__id_attr__]
    del clean_data[User.__password_attr__]
    # convert binary into string for easier json encoding
    clean_data[User.__token_attr__] = str(user_data[User.__token_attr__])
    return clean_data

# TODO: Adapters?
def clean_up_input(user_data: dict) -> dict:
    user_data = dict(user_data)
    password = user_data[User.__password_attr__]
    user_data[User.__password_attr__] = encrypt(password)
    if User.__id_attr__ in user_data and user_data[User.__id_attr__] is None:
        del user_data[User.__id_attr__]
    return user_data


def operation_set(**kwargs):
    return {'$set': kwargs}
