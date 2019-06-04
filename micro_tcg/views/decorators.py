from aiohttp import web

from micro_tcg.models import User


def b_string_to_bytes(b_str: str) -> bytes:
    """ converts a string containing a bytes literal (ex: 'b"something"') to bytes. """
    return b_str[2:-1].encode()


def db_operation(view):
    """ invokes decorated function with an extra 'db' parameter. """
    async def wrapper(request):
        db = request.app['db']
        return await view(request, db)
    return wrapper


def require_auth(view):
    """ invokes decorated function if the user is authenticated. 401 otherwise. """
    @db_operation
    async def wrapper(request, db):
        try:
            json_request = await request.json()
            token = json_request['token']
            token = b_string_to_bytes(token)
            user = await User.validate_token(db, token)
            if user is None:
                raise
            return await view(request)
        except Exception as e:
            print(e)
            return web.json_response('unauthorized user', status=401)
    return wrapper


def require_auth_web_socket(view):
    """ invokes decorated function if the user is authenticated. json informing 401 otherwise. """
    @db_operation
    async def wrapper(request, db):
        socket = web.WebSocketResponse()
        await socket.prepare(request)
        request_json = await socket.receive_json()
        token = request_json['token']
        token = b_string_to_bytes(token)
        user = await User.validate_token(db, token)
        if user is None:
            await socket.send_json(dict(
                message='unauthorized user',
                status=401
            ))
            return socket
        return await view(request, socket, user)
    return wrapper
