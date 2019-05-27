from aiohttp import web
from micro_tcg.routes import setup_routes
from motor.motor_asyncio import AsyncIOMotorClient


def create_app(db=None):
    _app = web.Application()
    _app['db'] = db if db is not None else AsyncIOMotorClient().micro_tcg
    setup_routes(_app)
    return _app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app)
