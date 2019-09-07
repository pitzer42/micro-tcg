from typing import NoReturn

from engine.models.remote_player import RemotePlayer


class WebSocketPlayer(RemotePlayer):

    def __init__(self, socket):
        self.socket = socket

    async def send(self, message: str) -> NoReturn:
        await self.socket.send_json(message)

    async def receive(self) -> str:
        return await self.socket.receive_json()
