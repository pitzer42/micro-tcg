from aiohttp import web
from micro_tcg.routes import setup_routes
from motor.motor_asyncio import AsyncIOMotorClient
from micro_tcg.views.match import WaitingList


def create_app(db=None):
    new_app = web.Application()
    if db is None:
        db = AsyncIOMotorClient().micro_tcg
    new_app['db'] = db

    # in memory data structure
    new_app['waiting_list'] = WaitingList(2)

    setup_routes(new_app)
    return new_app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app)
