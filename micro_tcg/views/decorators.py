from aiohttp import web

from micro_tcg.models import User


def b_string_to_bytes(b_str: str) -> bytes:
    """ converts a string containing a bytes literal (ex: 'b"something"') to bytes. """
    return b_str[2:-1].encode()


def inject_json(view):
    async def wrapper(request, *args, **kwargs):
        kwargs['json'] = await request.json()
        return await view(request, *args, **kwargs)
    return wrapper


def inject_db(view):
    async def wrapper(request, *args, **kwargs):
        kwargs['db'] = request.app['db']
        return await view(request, *args, **kwargs)
    return wrapper


def inject_socket(view):
    async def wrapper(request, *args, **kwargs):
        socket = web.WebSocketResponse()
        await socket.prepare(request)
        kwargs['socket'] = socket
        return await view(request, *args, **kwargs)
    return wrapper


def inject_waiting_list(view):
    async def wrapper(request, *args, **kwargs):
        kwargs['waiting_list'] = request.app['waiting_list']
        return await view(request, *args, **kwargs)
    return wrapper


def require_auth(view):
    """ invokes decorated function if the user_repo is authenticated. 401 otherwise. """
    @inject_db
    @inject_json
    async def wrapper(request, *args, db=None, json=None, **kwargs):
        try:
            token = json['token']
            token = b_string_to_bytes(token)
            user = await User.validate_token(db, token)
            if user is None:
                raise
            kwargs['user_repo'] = user
            kwargs['db'] = db
            kwargs['json'] = json
            return await view(
                request,
                *args,
                **kwargs
            )
        except Exception as e:
            print(e)
            return web.json_response('unauthorized user_repo', status=401)
    return wrapper


def require_auth_web_socket(view):
    """ invokes decorated function if the user_repo is authenticated. json informing 401 otherwise. """
    @inject_db
    @inject_socket
    async def wrapper(request, *args, db=None, socket=None, **kwargs):
        json = await socket.receive_json()
        token = json['token']
        token = b_string_to_bytes(token)
        user = await User.validate_token(db, token)
        if user is None:
            await socket.send_json(dict(
                message='unauthorized user_repo',
                status=401
            ))
            return socket
        kwargs['user'] = user
        kwargs['db'] = db
        kwargs['socket'] = socket
        return await view(
            request,
            *args,
            **kwargs
        )
    return wrapper
