from aiohttp.web import json_response

__socket_key__ = 'socket'
__json_key__ = 'json'
__db_key__ = 'db'
__waiting_list_key__ = 'waiting_list'
__game_loop_key__ = 'game_loop'
__token_key__ = 'token'
__user_key__ = 'user'


async def read_json(request, *args, **kwargs):
    if __socket_key__ in kwargs:
        socket = kwargs[__socket_key__]
        return await socket.receive_json()
    return await request.json()


async def send_json(data: dict, *args, **kwargs):
    if __socket_key__ in kwargs:
        socket = kwargs[__socket_key__]
        await socket.send_json(data)
        return socket
    return json_response(data)


async def unauthorized(*args, **kwargs):
    response = dict(
        message='unauthorized',
        status=401
    )
    return await send_json(response, *args, **kwargs)

