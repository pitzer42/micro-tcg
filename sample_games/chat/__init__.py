from engine.io.gamepad import Gamepad
from engine.io.connection_group import ConnectionGroup
from engine.io.client_connection import ClientConnection


async def chat_loop(main_client: ClientConnection, all_clients: ConnectionGroup):

    other_clients = all_clients.but(main_client)
    other_names = [other._id for other in other_clients]
    welcome_message = ', '.join(other_names)
    welcome_package = dict(message=welcome_message)

    try:
        await main_client.send(welcome_package)
        async for package in main_client.socket:
            message = package.data
            print(main_client._id + ':' + message)
            await all_clients.multicast(main_client, package)
    except IOError as error:
        print(error)


class ChatGamepad(Gamepad):

    def __init__(self, *args, **kwargs):
        Gamepad.__init__(self, *args, **kwargs)
        self.other_clients_in_chat: str = None

    async def start(self):
        await Gamepad.start(self)
        others = await self.receive_and_print()
        self.other_clients_in_chat = others['message']
        return others