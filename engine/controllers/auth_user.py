import time

from engine.models.user import User
from engine.repos.users import Users

from engine.crypt import (
    encrypt,
    equals_to_encrypted
)


async def login(users: Users, name: str, password: str):
    user_data = await users.get_by_name(name)
    if user_data is None:
        return
    password_hash = user_data[User._password_attr]
    if not equals_to_encrypted(password, password_hash):
        return
    user_id = user_data[User._id_attr]
    token = get_timestamp() + str(user_id)
    token = encrypt(token)
    await users.set_token(user_id, token)
    return token


async def validate_token(users: Users, token):
    user = await users.get_by_token(token)
    return user


async def logout(users: Users, token):
    await users.replace_token(token, None)


def get_timestamp() -> str:
    timestamp = time.time()
    timestamp = int(timestamp)
    return str(timestamp)


