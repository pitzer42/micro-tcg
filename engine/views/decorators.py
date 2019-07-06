from aiohttp import web

from engine.controllers.auth_user import validate_token

from engine.views import (
    read_json,
    unauthorized,
    __socket_key__,
    __json_key__,
    __repositories_key__,
    __waiting_list_key__,
    __game_loop_key__,
    __token_key__,
    __user_key__
)


def require_socket(view):
    async def wrapper(request, *args, **kwargs):
        socket = web.WebSocketResponse()
        await socket.prepare(request)
        kwargs[__socket_key__] = socket
        return await view(request, *args, **kwargs)
    return wrapper


def require_json(view):
    async def wrapper(request, *args, **kwargs):
        kwargs[__json_key__] = await read_json(request, *args, **kwargs)
        return await view(request, *args, **kwargs)
    return wrapper


def require_repositories(view):
    async def wrapper(request, *args, **kwargs):
        kwargs[__repositories_key__] = request.app[__repositories_key__]
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


def require_auth(view):
    """ invokes decorated function if the user_repo is authenticated. 401 otherwise. """

    @require_json
    @require_repositories
    async def wrapper(request, *args, json=None, repositories=None, **kwargs):
        kwargs[__repositories_key__] = repositories
        kwargs[__json_key__] = json

        token = json.get(__token_key__)
        if not token:
            return await unauthorized(request, *args, **kwargs)

        token = b_string_to_bytes(token)
        authenticated_user = await validate_token(repositories.users, token)
        if not authenticated_user:
            return await unauthorized(request, *args, **kwargs)

        kwargs[__user_key__] = authenticated_user
        return await view(
            request,
            *args,
            **kwargs
        )

    return wrapper


def b_string_to_bytes(b_str: str) -> bytes:
    """ converts a string containing a bytes literal (ex: 'b"something"') to bytes. """
    return b_str[2:-1].encode()
