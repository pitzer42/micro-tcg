import asyncio

from engine.io.client_connection import ClientConnection
from engine.io.connection_group import ConnectionGroup

from engine.server import (
    create_game_server,
    run_game_server
)

rules = {
    'p': 'r',
    'r': 's',
    's': 'p'
}

header = 'choose your move \n p - paper \n r - rock \n s - scissors'


async def jokenpo_loop(player: ClientConnection, all_players: ConnectionGroup):
    # first player`s loop does the job. All others can wait.
    game_over = asyncio.Event()
    if all_players.clients[0] != player:
        return await game_over.wait()

    for a in all_players:
        for b in all_players:
            if a != b:

                move_a = ''
                while move_a not in rules.keys():
                    await a.send(header)
                    move_a = await a.receive()
                    print(move_a)
                    move_a = move_a['message']

                move_b = ''
                while move_b not in rules.keys():
                    await b.send(header)
                    move_b = await b.receive()
                    print(move_b)
                    move_b = move_b['message']

                if rules[move_a] == move_b:
                    await a.send('you won by playing '+move_a+' against '+move_b)
                    await b.send('you lost by playing ' + move_b + ' against ' + move_a)
                else:
                    await a.send('you lost by playing ' + move_a + ' against ' + move_b)
                    await b.send('you won by playing ' + move_b + ' against ' + move_a)
    game_over.set()


if __name__ == '__main__':
    app = create_game_server(game_loop=jokenpo_loop)
    run_game_server(app)
