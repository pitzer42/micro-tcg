from engine.io.connection_group import ConnectionGroup
from engine.io.client_connection import ClientConnection


async def game_loop(player: ClientConnection, all_players: ConnectionGroup):
    def welcome_message_for(client: ClientConnection):
        other_names = ''
        for other in all_players.clients:
            if client is other:
                continue
            other_names += other._id + ', '
        other_names = other_names[0:-2]
        if ',' in other_names:
            print()
        return dict(message=other_names)

    try:
        message_package = welcome_message_for(player)
        await player.send(message_package)
        async for package in player.socket:
            message = package.data
            print(player._id + ':' + message)
            await all_players.multicast(player, package)
    except IOError as error:
        print(error)