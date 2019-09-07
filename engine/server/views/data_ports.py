import engine.repositories.schemas.user_schema as schema


def user_to_secure_json_serializable_dict(user_data: dict) -> dict:
    user_data = dict(user_data)
    del user_data[schema.object_id]
    del user_data[schema.token]
    del user_data[schema.password]
    return user_data


def json_to_credentials(json: dict) -> tuple:
    return (
        json[schema.name],
        json[schema.password]
    )


def token_to_authentication_json(token: str) -> dict:
    return {
        schema.token: str(token)
    }
