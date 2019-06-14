from aiohttp import web

from micro_tcg.controllers import auth_user

from micro_tcg.views.decorators import (
    require_auth,
    inject_db,
    inject_json
)

from micro_tcg.storage import user_repo


@inject_db
@inject_json
async def insert_one(request, db=None, json=None):
    try:
        inserted_id = await user_repo.insert(db, json)
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


@inject_db
async def list_all(request, db=None):
    try:
        users = await user_repo.list_all(db, limit=100)
        response_data = dict(
            status=200,
            users=users
        )
        return web.json_response(response_data)
    except Exception as e:
        response_data = dict(
            status=500,
            message=str(e)
        )
        return web.json_response(response_data)


@inject_db
@inject_json
async def login(request, db=None, json=None):
    name = json['name']
    password = json['password']
    token = await auth_user.login(db, name, password)
    if token is None:
        response_data = dict(message='Wrong credentials', status=401)
        return web.json_response(response_data)
    token = str(token)
    response_data = dict(token=token)
    return web.json_response(response_data)


@require_auth
async def protected_view(*args, **kwargs):
    return web.json_response('authorized')
