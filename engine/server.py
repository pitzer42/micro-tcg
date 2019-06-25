__db_key__ = 'db'
__game_loop_key__ = 'game_loop'
__waiting_list_key__ = 'waiting_list'

__default_waiting_list_size__ = 2
__default_host__ = '127.0.0.1'
__default_port__ = 8080

from aiohttp import web
from engine.routes import setup_routes
from motor.motor_asyncio import AsyncIOMotorClient
from engine.models.waiting_list import WaitingList


def create_game_server(
        db=None,
        waiting_list=None,
        game_loop=None):

    async def default_game_loop(*args, **kwargs):
        pass

    new_app = web.Application()

    if db is None:
        db = AsyncIOMotorClient().micro_tcg
    new_app[__db_key__] = db

    if game_loop is None:
        game_loop = default_game_loop
    new_app[__game_loop_key__] = game_loop

    if waiting_list is None:
        waiting_list = WaitingList(__default_waiting_list_size__)
    new_app[__waiting_list_key__] = waiting_list

    setup_routes(new_app)

    return new_app


def run_game_server(app, host=__default_host__, port=__default_port__):
    return web.run_app(
        app,
        host=host,
        port=port
    )



