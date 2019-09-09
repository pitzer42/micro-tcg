from engine.server import (
    create_game_app,
    run_game_server
)

if __name__ == '__main__':
    server = create_game_app()
    run_game_server(server)

