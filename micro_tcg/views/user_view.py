from aiohttp import web

from micro_tcg.controllers import auth_user

from micro_tcg.views.decorators import (
    require_auth,
    extract_db,
    extract_json
)

from micro_tcg.models.user import (
    __name_attr__,
    __password_attr__
)

from micro_tcg.storage.user_repo import (
    insert,
    list_all
)


@extract_db
@extract_json
async def insert_one(request, db=None, json=None):
    try:
        inserted_id = await insert(db, json)
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


@extract_db
async def list_all(request, db=None):
    try:
        users = await list_all(db, limit=100)
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


@extract_db
@extract_json
async def login(request, db=None, json=None):
    name = json[__name_attr__]
    password = json[__password_attr__]
    token = await auth_user.login(db, name, password)
    if token is None:
        response_data = dict(
            message='Wrong credentials',
            status=401
        )
        return web.json_response(response_data)
    token = str(token)
    response_data = dict(token=token)
    return web.json_response(response_data)


@require_auth
async def protected_view(*args, **kwargs):
    return web.json_response('authorized')
