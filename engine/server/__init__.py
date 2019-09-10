import aiohttp_cors
from aiohttp import web

from motor.motor_asyncio import AsyncIOMotorClient

from engine.models.remote_party import PartyFactory
from engine.models.game_loop import default_game_loop

from engine.repositories_mongo.mongo_user_repository import MongoUserRepository

import engine.server.app_schema
from engine.server.views.user_view import UserView
from engine.server.views.game_view import GameView
from engine.server.views.auth_view import AuthView


def _create_cors(app: web.Application):
    wildcard = '*'
    options = aiohttp_cors.ResourceOptions(
        expose_headers=wildcard,
        allow_headers=wildcard
    )
    defaults = {wildcard: options}
    return aiohttp_cors.setup(app, defaults=defaults)


def create_game_app(
        db=AsyncIOMotorClient().micro_tcg,
        user_repo_factory=MongoUserRepository,
        game_loop=default_game_loop):

    users = user_repo_factory(db)

    app = web.Application()
    app[app_schema.user_repo] = users
    app[app_schema.party_factory] = PartyFactory(2)
    app[app_schema.game_loop] = game_loop

    cors = _create_cors(app)

    view_register = [
        UserView,
        GameView,
        AuthView
    ]

    for view in view_register:
        resource = app.router.add_view(view.__route__, view)
        cors.add(resource)

    return app


def start_game_server(game_app):
    web.run_app(game_app)
