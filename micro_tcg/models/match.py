from micro_tcg.io.user_io import (
    ClientConnection,
    ConnectionGroup
)
from micro_tcg.models import assign_dict_to_obj


class Match:

    __clients_attr__ = 'clients'

    def __init__(self, **kwargs):
        setattr(self, Match.__clients_attr__, ConnectionGroup(list()))
        self.running = False
        assign_dict_to_obj(self, **kwargs)

    async def game_loop(self):
        pass

    async def start(self, client: ClientConnection):
        try:
            message_package = self.welcome_message_for(client)
            await client.send(message_package)
            async for package in client.socket:
                message = package.data
                print(client.name + ':' + message)
                await self.clients.multicast(client, package)
        except IOError as error:
            print(error)

    def welcome_message_for(self, client: ClientConnection):
        other_names = ''
        for other in self.clients.clients:
            if client is other:
                continue
            other_names += other._id + ', '
        other_names = other_names[0:-2]
        return dict(message=other_names)
