from aiohttp import web

from engine.views import (
    unauthorized,
    __socket_key__,
    __json_key__,
    __db_key__,
    __waiting_list_key__,
    __game_loop_key__,
    __token_key__,
    __user_key__,
    read_json
)

from engine.controllers.auth_user import validate_token


def b_string_to_bytes(b_str: str) -> bytes:
    """ converts a string containing a bytes literal (ex: 'b"something"') to bytes. """
    return b_str[2:-1].encode()


def require_json(view):
    async def wrapper(request, *args, **kwargs):
        kwargs[__json_key__] = await read_json(request, *args, **kwargs)
        return await view(request, *args, **kwargs)
    return wrapper


def require_db(view):
    async def wrapper(request, *args, **kwargs):
        kwargs[__db_key__] = request.app[__db_key__]
        return await view(request, *args, **kwargs)
    return wrapper


def require_waiting_list(view):
    async def wrapper(request, *args, **kwargs):
        kwargs[__waiting_list_key__] = request.app[__waiting_list_key__]
        return await view(request, *args, **kwargs)
    return wrapper


def require_game_loop(view):
    async def wrapper(request, *args, **kwargs):
        kwargs[__game_loop_key__] = request.app[__game_loop_key__]
        return await view(request, *args, **kwargs)
    return wrapper


def web_socket_view(view):
    async def wrapper(request, *args, **kwargs):
        socket = web.WebSocketResponse()
        await socket.prepare(request)
        kwargs[__socket_key__] = socket
        return await view(request, *args, **kwargs)
    return wrapper


def require_auth(view):
    """ invokes decorated function if the user_repo is authenticated. 401 otherwise. """
    @require_db
    @require_json
    async def wrapper(request, *args, db=None, json=None, **kwargs):
        kwargs[__db_key__] = db
        kwargs[__json_key__] = json

        token = json.get(__token_key__)
        if not token:
            return await unauthorized(request, *args, **kwargs)

        token = b_string_to_bytes(token)
        authenticated_user = await validate_token(db, token)
        if not authenticated_user:
            return await unauthorized(request, *args, **kwargs)

        kwargs[__user_key__] = authenticated_user
        return await view(
            request,
            *args,
            **kwargs
        )

    return wrapper
