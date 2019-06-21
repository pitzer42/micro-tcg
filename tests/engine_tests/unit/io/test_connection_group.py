import unittest

from tests.engine_tests import run_async
from tests.engine_tests.mocks.mock_socket import SocketMock

from engine.io.client_connection import ClientConnection
from engine.io.connection_group import ConnectionGroup

default_group_size = 3


def create_connection_group():
    client_sockets = [SocketMock() for i in range(default_group_size)]
    clients = [ClientConnection(i, client_sockets[i]) for i in range(default_group_size)]
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

    def test_group_has_size_property(self):
        group = create_connection_group()

        def set_size():
            group.size = 0

        self.assertRaises(Exception, set_size)
        self.assertEqual(group.size, default_group_size)

    def test_get_connected_clients(self):
        group = create_connection_group()
        connected_clients = group.get_connected_clients()
        for client in connected_clients:
            self.assertTrue(client.is_connected)
            client.socket.connected = False
        connected_clients = group.get_connected_clients()
        self.assertEqual(len(connected_clients), 0)

    def test_connection_group_is_iterable(self):
        group = create_connection_group()
        counter = 0
        for _ in group:
            counter += 1
        self.assertEqual(counter, default_group_size)

    def test_back_reference_from_client_connection_to_connection_group(self):
        group = create_connection_group()
        for client in group:
            self.assertEqual(client.group, group)
