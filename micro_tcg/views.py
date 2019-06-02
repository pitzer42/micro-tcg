from aiohttp import web
from micro_tcg.models import User
from aiohttp import WSMsgType


class Match:

    waiting_list = dict()

    @staticmethod
    async def make_match():
        # enough players for at least one match
        while len(Match.waiting_list) > 1:

            # two items make a match
            token_a, socket_a = Match.waiting_list.popitem()
            token_b, socket_b = Match.waiting_list.popitem()
            try:
                match_a = dict(opponent=token_b)
                match_b = dict(opponent=token_a)
                if socket_a.closed or socket_b.closed:
                    raise IOError
                await socket_a.send_json(match_a)
                await socket_b.send_json(match_b)
            except IOError:

                # something went wrong, keep the items that still active and continue
                if not socket_a.closed:
                    Match.waiting_list[token_a] = socket_a
                if not socket_b.closed:
                    Match.waiting_list[token_b] = socket_b


def b_string_to_bytes(b_str: str) -> bytes:
    """ converts a string containing a bytes literal (ex: 'b"something"') to bytes. """
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


def require_auth_websocket(view):
    async def wrapper(request):
        socket = web.WebSocketResponse()
        await socket.prepare(request)
        request_json = await socket.receive_json()
        token = b_string_to_bytes(request_json['token'])
        db = request.app['db']
        user = await User.validate_token(db, token)

        if user is None:
            await socket.send_json(dict(
                message='unauthorized user',
                status=401
            ))
            return socket
        return await view(socket, user)
    return wrapper


@require_auth_websocket
async def enter_waiting_list(socket, user):
    ack_json = dict(
        message='you are now in the waiting list'
    )
    await socket.send_json(ack_json)
    Match.waiting_list[user.username] = socket

    await Match.make_match()

    async for message in socket:
        if message.type == WSMsgType.TEXT:
            if message.data == 'close':
                await socket.close()
            else:
                print(message)
        elif message.type == WSMsgType.ERROR:
            print('%s connection closed with exception %s' % (
                user.username,
                socket.exception()
            ))

    print('closed connection with %s' % user.username)
    return socket

