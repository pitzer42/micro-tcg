from aiohttp import web

import engine.storage.user_repo as users

from engine.models.user import User
from engine.controllers import auth_user

from engine.views import unauthorized

from engine.views.decorators import (
    require_auth,
    require_db,
    require_json
)


@require_db
@require_json
async def insert_one(request, db=None, json=None):
    try:
        inserted_id = await users.insert(db, json)
        response_data = dict(
            status=200,
            inserted_id=inserted_id
        )
        return web.json_response(response_data)
    except Exception as e:
        response_data = dict(
            status=500,
            message=str(e)
        )
        return web.json_response(response_data)


@require_db
async def list_all(request, db=None):
    try:
        all_users = await users.list_all(db, limit=100)
        response_data = dict(
            status=200,
            users=all_users
        )
        return web.json_response(response_data)
    except Exception as e:
        response_data = dict(
            status=500,
            message=str(e)
        )
        return web.json_response(response_data)


@require_db
@require_json
async def login(request, db=None, json=None):
    name = json[User.__name_attr__]
    password = json[User.__password_attr__]
    token = await auth_user.login(db, name, password)
    if token is None:
        return await unauthorized(request)
    token = str(token)
    response_data = dict(token=token)
    return web.json_response(response_data)


@require_auth
async def protected_view(*args, **kwargs):
    return web.json_response('authorized')
