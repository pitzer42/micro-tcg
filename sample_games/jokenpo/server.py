from sample_games.jokenpo import jokenpo_loop

from engine.server import (
    create_game_server,
    run_game_server
)


if __name__ == '__main__':
    app = create_game_server(game_loop=jokenpo_loop)
    run_game_server(app)
