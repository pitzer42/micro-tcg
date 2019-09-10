from typing import NoReturn

from engine.models.remote_party import RemoteParty
from engine.models.remote_player import RemotePlayer


async def default_game_loop(player: RemotePlayer, party: RemoteParty) -> NoReturn:
    raise NotImplemented()
