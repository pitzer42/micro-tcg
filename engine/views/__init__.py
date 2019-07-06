from aiohttp.web import json_response

__socket_key__ = 'socket'
__json_key__ = 'json'
__db_key__ = 'db'
__waiting_list_key__ = 'waiting_list'
__game_loop_key__ = 'game_loop'
__token_key__ = 'token'
__user_key__ = 'user'


async def unauthorized(request, *args, **kwargs):
    response = dict(
        message='unauthorized',
        status=401
    )

    if __socket_key__ in kwargs:
        socket = kwargs[__socket_key__]
        await socket.send_json(response)
        return socket
    return json_response(response)


