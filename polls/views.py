from aiohttp import web
from polls.models import User


async def put_user(request):
    db = request.app['db']
    json_data = await request.json()
    new_user = User(**json_data)
    await new_user.save(db)
    return web.json_response('ok')


async def get_users(request):
    db = request.app['db']
    collection = User.get_collection(db)
    users = await collection.find().to_list(length=100)
    for user in users:
        del user['_id']
        del user['password']
    return web.json_response(users)
