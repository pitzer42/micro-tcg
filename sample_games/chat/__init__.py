from engine.client import Gamepad
from engine.io.client_connection import ClientConnection


async def chat_loop(main_client: ClientConnection):

    other_clients = main_client.group.except_for(main_client)
    other_names = [other._id for other in other_clients]
    welcome_message = ', '.join(other_names)
    welcome_package = dict(message=welcome_message)

    try:
        await main_client.send(welcome_package)
        async for package in main_client.socket:
            message = package.data
            print(main_client._id + ':' + message)
            await main_client.group.multicast(main_client, package)
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