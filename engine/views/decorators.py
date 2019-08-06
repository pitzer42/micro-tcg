from aiohttp import web

from json.decoder import JSONDecodeError

from engine.controllers.auth_user import validate_token

from engine.views import (
    read_json,
    unauthorized,
    SOCKET_KEY,
    JSON_KEY,
    REPOSITORIES_KEY,
    WAITING_LIST_KEY,
    GAME_LOOP_KEY,
    TOKEN_KEY,
    USER_KEY
)


def require_socket(view):
    async def wrapper(request, *args, **kwargs):
        socket = web.WebSocketResponse()
        await socket.prepare(request)
        kwargs[SOCKET_KEY] = socket
        return await view(request, *args, **kwargs)
    return wrapper


def require_json(view):
    async def wrapper(request, *args, **kwargs):
        try:
            kwargs[JSON_KEY] = await read_json(request, *args, **kwargs)
        except JSONDecodeError:
            kwargs[JSON_KEY] = None
        return await view(request, *args, **kwargs)
    return wrapper


def require_repositories(view):
    async def wrapper(request, *args, **kwargs):
        kwargs[REPOSITORIES_KEY] = request.app[REPOSITORIES_KEY]
        return await view(request, *args, **kwargs)
    return wrapper


def require_waiting_list(view):
    async def wrapper(request, *args, **kwargs):
        kwargs[WAITING_LIST_KEY] = request.app[WAITING_LIST_KEY]
        return await view(request, *args, **kwargs)
    return wrapper


def require_game_loop(view):
    async def wrapper(request, *args, **kwargs):
        kwargs[GAME_LOOP_KEY] = request.app[GAME_LOOP_KEY]
        return await view(request, *args, **kwargs)
    return wrapper


def require_auth(view):
    """ invokes decorated function if the user_repo is authenticated. 401 otherwise. """

    @require_json
    @require_repositories
    async def wrapper(request, *args, json=None, repositories=None, **kwargs):
        kwargs[REPOSITORIES_KEY] = repositories
        kwargs[JSON_KEY] = json

        token = json.get(TOKEN_KEY)
        if not token:
            return await unauthorized(request, *args, **kwargs)

        token = b_string_to_bytes(token)
        authenticated_user = await validate_token(repositories.users, token)
        if not authenticated_user:
            return await unauthorized(request, *args, **kwargs)

        kwargs[USER_KEY] = authenticated_user
        return await view(
            request,
            *args,
            **kwargs
        )

    return wrapper


def b_string_to_bytes(b_str: str) -> bytes:
    """ converts a string containing a bytes literal (ex: 'b"something"') to bytes. """
    return b_str[2:-1].encode()
