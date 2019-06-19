import unittest

from tests import run_async
from tests.mocks.mock_socket import SocketMock

from micro_tcg.io.client_connection import ClientConnection
from micro_tcg.io.connection_group import ConnectionGroup


def create_connection_group(size=3):
    client_sockets = [SocketMock() for i in range(size)]
    clients = [ClientConnection(i, client_sockets[i]) for i in range(size)]
    return ConnectionGroup(clients)


class TestConnectionGroup(unittest.TestCase):

    @run_async
    async def test_broadcast(self):
        message = dict(message='message')
        group = create_connection_group()
        await group.broadcast(message)
        for client in group.clients:
            self.assertIn(message, client.socket.sent_messages)

    @run_async
    async def test_multicast(self):
        message = dict(message='message')
        group = create_connection_group()
        emitter = group.clients[0]
        await group.multicast(emitter, message)
        for client in group.clients:
            if client != emitter:
                self.assertIn(message, client.socket.sent_messages)
            else:
                self.assertNotIn(message, client.socket.sent_messages)

    def test_get_connected_clients(self):
        group = create_connection_group()
        connected_clients = group.get_connected_clients()
        for client in connected_clients:
            self.assertTrue(client.is_connected)
            client.socket.connected = False
        connected_clients = group.get_connected_clients()
        self.assertEqual(len(connected_clients), 0)


