from aiohttp import web
from micro_tcg.models import User
from micro_tcg.views.decorators import (
    db_operation,
    require_auth,
)


@db_operation
async def insert_one(request, db):
    json_data = await request.json()
    new_user = User(**json_data)
    await new_user.save(db)
    return web.json_response('ok')


@db_operation
async def list_all(request, db):
    collection = User.get_collection(db)
    users = await collection.find().to_list(length=100)
    for user in users:
        del user['_id']
        del user['password']
        user['token'] = str(user['token'])
    return web.json_response(users)


@db_operation
async def login(request, db):
    json_request = await request.json()
    username = json_request['username']
    password = json_request['password']
    user = await User.auth_or_none(db, username, password)
    if user is None:
        response_data = dict(message='Wrong credentials', status=401)
        return web.json_response(response_data)
    response_data = dict(token=str(user.token))
    return web.json_response(response_data)


@require_auth
async def protected_view(*args):
    return web.json_response('authorized')
