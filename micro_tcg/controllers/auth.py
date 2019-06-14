import time

from micro_tcg.storage.user_repo import (
    get_by_username,
    update_token
)

from micro_tcg.crypto import (
    encrypt,
    equals_to_encrypted
)


def get_timestamp() -> str:
    timestamp = time.time()
    timestamp = int(timestamp)
    return str(timestamp)


def login(db, username: str, password: str):
    user_data = get_by_username(db, username)
    if user_data is None:
        return
    password_hash = user_data['password']
    if not equals_to_encrypted(password_hash, password):
        return
    user_id = user_data['_id']
    token = get_timestamp() + user_id
    token = encrypt(token)
    await update_token(db, user_id, token)
    return token



"""
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
"""