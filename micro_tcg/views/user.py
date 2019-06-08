from aiohttp import web

from micro_tcg.models import User
from micro_tcg.views.decorators import (
    require_auth,
    inject_db,
    inject_json
)


@inject_db
@inject_json
async def insert_one(request, db=None, json=None):
    new_user = User(**json)
    await new_user.save(db)
    return web.json_response('ok')


@inject_db
async def list_all(request, db=None):
    collection = User.get_collection(db)
    users = await collection.find().to_list(length=100)
    for user in users:
        # remove _id and password from the payload
        del user['_id']
        del user['password']
        user['token'] = str(user['token'])
    return web.json_response(users)


@inject_db
@inject_json
async def login(request, db=None, json=None):
    username = json['username']
    password = json['password']
    user = await User.auth_or_none(db, username, password)
    if user is None:
        response_data = dict(message='Wrong credentials', status=401)
        return web.json_response(response_data)
    response_data = dict(token=str(user.token))
    return web.json_response(response_data)


@require_auth
async def protected_view(*args, **kwargs):
    return web.json_response('authorized')
