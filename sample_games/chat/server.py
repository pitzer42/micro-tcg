from engine.server import (
    create_game_server,
    run_game_server
)

from sample_games.chat import chat_loop


if __name__ == '__main__':
    server = create_game_server(game_loop=chat_loop)
    run_game_server(server)