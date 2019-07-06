from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient

from engine.routes import setup_routes
from engine.storage.mongo import MongoRepositories
from engine.models.waiting_list import WaitingList

__repositories_key__ = 'repositories'
__game_loop_key__ = 'game_loop'
__waiting_list_key__ = 'waiting_list'

__default_waiting_list_size__ = 2
__default_host__ = '127.0.0.1'
__default_port__ = 8080


async def __default_game_loop__(*args, **kwargs):
    pass


def __create_default_repositories__():
    db = AsyncIOMotorClient().micro_tcg
    return MongoRepositories(db)


def create_game_server(
        repositories=__create_default_repositories__(),
        waiting_list_size=__default_waiting_list_size__,
        game_loop=__default_game_loop__):

    new_app = web.Application()

    new_app[__game_loop_key__] = game_loop
    new_app[__repositories_key__] = repositories
    new_app[__waiting_list_key__] = WaitingList(waiting_list_size)

    setup_routes(new_app)

    return new_app


def run_game_server(app, host=__default_host__, port=__default_port__):
    return web.run_app(
        app,
        host=host,
        port=port
    )
