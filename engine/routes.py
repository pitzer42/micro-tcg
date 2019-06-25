from aiohttp.web import (
    get,
    put,
)

from engine.views import (
    user_view,
    match_view
)


users = '/users'
login = '/users/login'
secret = '/secret'
waiting_list = '/waiting_list'


def setup_routes(app):
    app.add_routes([
        get(users, user_view.list_all),
        put(users, user_view.insert_one),
        get(login, user_view.login),
        get(secret, user_view.protected_view),
        get(waiting_list, match_view.enter_waiting_list)
    ])
