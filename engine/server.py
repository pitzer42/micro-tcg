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
    new_app['db'] = db

    if game_loop is None:
        game_loop = default_game_loop
    new_app['game_loop'] = game_loop

    if waiting_list is None:
        waiting_list = WaitingList(2)
    new_app['waiting_list'] = waiting_list

    setup_routes(new_app)

    return new_app


def run_game_server(app, host='127.0.0.1', port=8080):
    return web.run_app(
        app,
        host=host,
        port=port
    )



