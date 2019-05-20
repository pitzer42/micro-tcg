from aiohttp.web import (get, put)
from polls.views import *


def setup_routes(app):
    app.add_routes([
        get('/users', get_users),
        put('/users', put_user)
    ])