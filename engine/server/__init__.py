import aiohttp_cors
from aiohttp import web

from motor.motor_asyncio import AsyncIOMotorClient

from engine.models.remote_party import PartyFactory

from engine.repositories_mongo.mongo_user_repository import MongoUserRepository

import engine.server.app_schema

from engine.server.views.user_view import UserView
from engine.server.views.game_view import GameView
from engine.server.views.auth_view import AuthView


def _default_game_loop(*args, **kwargs):
    pass


def _default_repo_factory():
    db = AsyncIOMotorClient().micro_tcg
    return MongoUserRepository(db)


def _create_cors(app: web.Application):
    wildcard = '*'
    options = aiohttp_cors.ResourceOptions(
        expose_headers=wildcard,
        allow_headers=wildcard
    )
    defaults = {wildcard: options}
    return aiohttp_cors.setup(app, defaults=defaults)


def create_game_app(
        user_repo_factory=_default_repo_factory,
        game_loop=_default_game_loop,
        party_size=2):

    app = web.Application()
    app[app_schema.user_repo] = user_repo_factory()
    app[app_schema.party_factory] = PartyFactory(party_size)
    app[app_schema.game_loop] = game_loop

    view_register = [
        UserView,
        GameView,
        AuthView
    ]

    cors = _create_cors(app)

    for view in view_register:
        resource = app.router.add_view(view.__route__, view)
        cors.add(resource)

    return app


def start_game_server(game_app):
    web.run_app(game_app)
