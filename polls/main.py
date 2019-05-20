from aiohttp import web
from polls.routes import setup_routes
from motor.motor_asyncio import AsyncIOMotorClient

app = web.Application()
app['db'] = AsyncIOMotorClient().micro_tcg
setup_routes(app)
web.run_app(app)
