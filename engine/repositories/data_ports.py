from bcrypt import (
    gensalt,
    hashpw
)

from engine.models.user import User

import engine.repositories.schemas.user_schema as schema


def pass_by(x):
    return x


def dict_to_user(raw_data: dict) -> User:
    return User(
        name=raw_data.get(schema.name),
        password=raw_data.get(schema.password),
        token=raw_data.get(schema.token)
    )


def user_to_password_hashed_dict(user: User) -> dict:
    return dict_to_password_hashed_dict(user.__dict__)


def dict_to_password_hashed_dict(raw_data: dict) -> dict:
    raw_data = dict(raw_data)
    clear_password = raw_data[schema.password]
    clear_password = str(clear_password).encode()
    raw_data[schema.password] = hashpw(
        clear_password,
        gensalt()
    )
    return raw_data
