from aiohttp import web
from micro_tcg.routes import setup_routes
from motor.motor_asyncio import AsyncIOMotorClient
from micro_tcg.models.waiting_list import WaitingList


def create_aiohttp_app(
        db=None,
        waiting_list=None,
        game_loop=None):

    async def default_game_loop(*args, **kwargs):
        pass

    new_app = web.Application()

    new_app['db'] = db if db is not None else AsyncIOMotorClient().micro_tcg
    new_app['waiting_list'] = waiting_list if waiting_list is not None else WaitingList(2)
    new_app['game_loop'] = game_loop if game_loop is not None else default_game_loop

    setup_routes(new_app)

    return new_app


def run_aiohttp_app(app, host='127.0.0.1', port=8080):
    return web.run_app(
        app,
        host=host,
        port=port
    )



