from engine.io.client_connection import ClientConnection
from engine.models.waiting_list import WaitingList


async def play_next_match(
        player: ClientConnection,
        waiting_list: WaitingList,
        game_loop):
    all_players = await waiting_list.next_group(player)
    await game_loop(player, all_players)
