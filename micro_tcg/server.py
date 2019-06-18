from aiohttp import web
from micro_tcg.routes import setup_routes
from motor.motor_asyncio import AsyncIOMotorClient
from micro_tcg.models.waiting_list import WaitingList


def create_aiohttp_app(db=None):
    new_app = web.Application()

    if db is None:
        db = AsyncIOMotorClient().micro_tcg
    new_app['db'] = db

    # in memory data structure
    new_app['waiting_list'] = WaitingList(2)

    setup_routes(new_app)
    return new_app


def run_aiohttp_app(app, host='127.0.0.1', port=8080):
    return web.run_app(
        app,
        host=host,
        port=port
    )



