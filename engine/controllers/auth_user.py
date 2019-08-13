import time

from engine.models.user import User
from engine.repos.users import Users

from engine.crypt import (
    encrypt,
    equals_to_encrypted
)


async def login(users: Users, name: str, password: str):
    user = await users.get_by_name(name)
    if user is None:
        return
    if not equals_to_encrypted(password, user.password):
        return
    token = get_timestamp() + str(user.uid)
    token = encrypt(token)
    await users.set_token(user.uid, token)
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


