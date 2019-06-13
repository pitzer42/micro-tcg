from micro_tcg.crypto import encrypt

__id_attr__ = '_id'
__storage_name__ = 'users'


async def count(db, query=dict()):
    collection = db[__storage_name__]
    return await collection.count_documents(query)


async def list_all(db, limit=100):
    collection = db[__storage_name__]
    cursor = collection.find()
    users_data = await cursor.to_list(length=limit)
    users = list()
    for user_data in users_data:
        clean_user_data = clean_up_output(user_data)
        users.append(clean_user_data)
    return users


async def insert(db, user_data: dict) -> int:
    user_data = clean_up_input(user_data)
    collection = db[__storage_name__]
    result = await collection.insert_one(user_data)
    return result.inserted_id


def clean_up_output(user_data: dict) -> dict:
    clean_data = dict(user_data)
    # remove _id and password from the payload
    del clean_data['_id']
    del clean_data['password']
    # convert binary into string for easier json encoding
    clean_data['token'] = str(user_data['token'])
    return clean_data


def clean_up_input(user_data: dict) -> dict:
    user_data = dict(user_data)
    password = user_data['password']
    user_data['password'] = encrypt(password)
    if __id_attr__ in user_data and user_data[__id_attr__] is None:
        del user_data[__id_attr__]
    return user_data

