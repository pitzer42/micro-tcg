from engine.server import (
    create_aiohttp_app,
    run_aiohttp_app
)

if __name__ == '__main__':
    app = create_aiohttp_app()
    run_aiohttp_app(app)
