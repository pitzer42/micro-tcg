
from engine.models.user import User
from engine.controllers import auth_user

from engine.views import unauthorized, send_json

from engine.views.decorators import (
    require_auth,
    require_repositories,
    require_json
)


@require_repositories
@require_json
async def insert_one(request, json=None, repositories=None, **kwargs):
    try:
        inserted_id = await repositories.users.insert(json)
        response_data = dict(
            status=200,
            inserted_id=str(inserted_id)
        )
        return await send_json(response_data, **kwargs)
    except Exception as e:
        response_data = dict(
            status=500,
            message=str(e)
        )
        return await send_json(response_data, **kwargs)


@require_repositories
async def list_all(request, repositories=None, **kwargs):
    try:
        all_users = await repositories.users.all(limit=100)
        response_data = dict(
            status=200,
            users=all_users
        )
        return await send_json(response_data, **kwargs)
    except Exception as e:
        response_data = dict(
            status=500,
            message=str(e)
        )
        return await send_json(response_data, **kwargs)

@require_json
@require_repositories
async def login(request, json=None, repositories=None, **kwargs):
    if None in (json, repositories):
        return await unauthorized(request)
    if User._name_attr not in json:
        return await unauthorized(request)
    name = json[User._name_attr]
    if User._password_attr not in json:
        return await unauthorized(request)
    password = json[User._password_attr]
    token = await auth_user.login(repositories.users, name, password)
    if token is None:
        return await unauthorized(request)
    token = str(token)
    response_data = dict(token=token)
    return await send_json(response_data, **kwargs)


@require_auth
async def protected_view(*args, **kwargs):
    return await send_json('authorized', **kwargs)
