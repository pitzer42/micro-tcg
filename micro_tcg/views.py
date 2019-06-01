from aiohttp import web
from micro_tcg.models import User


def b_string_to_bytes(b_str: str) -> bytes:
    """
    converts a string containing a bytes literal (ex: 'b"something"') to bytes.
    """
    return b_str[2:-1].encode()


def require_auth(view):
    async def wrapper(request):
        try:
            json_request = await request.json()
            token = json_request['token']
            token = b_string_to_bytes(token)
            query = dict(token=token)
            db = request.app['db']
            user = await User.get_collection(db).find_one(query)
            if user is None:
                raise
            return await view(request)
        except Exception as e:
            print(e)
            return web.json_response('unauthorized user', status=401)

    return wrapper


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
        user['token'] = str(user['token'])
    return web.json_response(users)


async def login_user(request):
    db = request.app['db']
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
async def protected_view(request):
    return web.json_response('authorized')
