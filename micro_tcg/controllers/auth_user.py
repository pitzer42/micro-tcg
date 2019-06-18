import time

from micro_tcg.models.user import User

from micro_tcg.storage.user_repo import (
    get_by_name,
    set_user_token,
    update_token,
    get_by_token
)

from micro_tcg.crypt import (
    encrypt,
    equals_to_encrypted
)


async def login(db, name: str, password: str):
    user_data = await get_by_name(db, name)
    if user_data is None:
        return
    password_hash = user_data[User.__password_attr__]
    if not equals_to_encrypted(password, password_hash):
        return
    user_id = user_data[User.__id_attr__]
    token = get_timestamp() + str(user_id)
    token = encrypt(token)
    await set_user_token(db, user_id, token)
    return token


async def validate_token(db, token):
    user = await get_by_token(db, token)
    return user is not None


async def logout(db, token):
    await update_token(db, token, None)


def get_timestamp() -> str:
    timestamp = time.time()
    timestamp = int(timestamp)
    return str(timestamp)


