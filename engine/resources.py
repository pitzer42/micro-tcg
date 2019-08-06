import aiohttp_cors

from engine.views import (
    user_view,
    match_view
)

GET = 'GET'
PUT = 'PUT'
WILDCARD = '*'

DEFAULT_CORS_OPTIONS = aiohttp_cors.ResourceOptions(
    expose_headers=WILDCARD,
    allow_headers=WILDCARD
)


class Resource:

    def __init__(self,
                 name=None,
                 path='/',
                 routes=None):
        self.name = str() if name is None else name
        self.path = path
        self.routes = dict(routes)
        self._aiohttp_resource = None
        self._aiohttp_routes = set()

    def register(self, router):
        self._aiohttp_resource = router.add_resource(self.path, name=self.name)
        for method, view in self.routes.items():
            aiohttp_route = self._aiohttp_resource.add_route(method, view)
            self._aiohttp_routes.add(aiohttp_route)

    def configure_cors(self, cors):
        cors.add(self._aiohttp_resource)
        for aiohttp_routes in self._aiohttp_routes:
            try:
                cors.add(aiohttp_routes)
            except ValueError:
                pass


users = Resource(
    name='users',
    path='/users',
    routes={
        GET: user_view.list_all,
        PUT: user_view.insert_one
    }
)

login = Resource(
    name='login',
    path='/login',
    routes={
        GET: user_view.login
    }
)

waiting_list = Resource(
    name='waiting_list',
    path='/waiting_list',
    routes={
        GET: match_view.enter_waiting_list
    }
)

secret = Resource(
    name='secret',
    path='/secret',
    routes={
        GET: user_view.protected_view
    }
)

_tracked_resources = [
    users,
    login,
    waiting_list,
    secret
]


def setup_routes(app):
    cors = aiohttp_cors.setup(app, defaults={
        WILDCARD: DEFAULT_CORS_OPTIONS
    })

    for resource in _tracked_resources:
        resource.register(app.router)
        resource.configure_cors(cors)
