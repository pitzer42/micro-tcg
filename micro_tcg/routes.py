from aiohttp.web import (get, put)
from micro_tcg.views import (user, match)


users = '/users'
login = '/users/login'
secret = '/secret'
waiting_list = '/waiting_list'


def setup_routes(app):
    app.add_routes([
        get(users, user.list_all),
        put(users, user.insert_one),
        get(login, user.login),
        get(secret, user.protected_view),
        get(waiting_list, match.enter_waiting_list)
    ])
