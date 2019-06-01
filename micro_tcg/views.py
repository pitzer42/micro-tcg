from aiohttp import web
from micro_tcg.models import User

waiting_list = dict()


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


async def enter_waiting_list(request):
    response = web.WebSocketResponse()
    await response.prepare(request)
    token = await response.receive()
    db = request.app['db']
    user = User.validate_token(db, token)

    if user is None:
        await response.send_json(dict(
            message='unauthorized user',
            status=401
        ))
        return response

    await response.send_str('you are now in the waiting list')

    waiting_list[token] = response
    while len(waiting_list) > 2:
        user_tokens = list(waiting_list.keys())
        token_a, token_b = user_tokens[0:2]
        socket_a = waiting_list[token_a]
        socket_b = waiting_list[token_b]
        await socket_a.send_str('match ' + token_b)
        await socket_b.send_str('match ' + token_a)
        del waiting_list[token_a]
        del waiting_list[token_b]

    return response

