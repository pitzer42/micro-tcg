from aiohttp.web import json_response

SOCKET_KEY = 'socket'
JSON_KEY = 'json'
REPOSITORIES_KEY = 'repositories'
WAITING_LIST_KEY = 'waiting_list'
GAME_LOOP_KEY = 'game_loop'
TOKEN_KEY = 'token'
USER_KEY = 'user'


async def read_json(request, *args, **kwargs):
    if SOCKET_KEY in kwargs:
        socket = kwargs[SOCKET_KEY]
        return await socket.receive_json()
    return await request.json()


async def send_json(data: dict, *args, **kwargs):
    if SOCKET_KEY in kwargs:
        socket = kwargs[SOCKET_KEY]
        await socket.send_json(data)
        return socket
    return json_response(data)


async def unauthorized(*args, **kwargs):
    response = dict(
        message='unauthorized',
        status=401
    )
    return await send_json(response, *args, **kwargs)

