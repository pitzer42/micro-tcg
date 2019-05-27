from aiohttp.web import (get, put)
from micro_tcg.views import *


def setup_routes(app):
    app.add_routes([
        get('/users', get_users),
        put('/users', put_user),
        get('/users/login', login_user),
        get('/secret', protected_view)
    ])