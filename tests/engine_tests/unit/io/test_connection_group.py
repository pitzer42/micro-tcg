import unittest

from tests import run_async
from tests.engine_tests.mocks.socket import SocketMock

from engine.io.client_connection import ClientConnection
from engine.io.connection_group import ConnectionGroup

__default_size__ = 3


def create_group(size=__default_size__):
    clients = list()
    for i in range(size):
        socket = SocketMock()
        client = ClientConnection(i, socket)
        clients.append(client)
    return ConnectionGroup(clients)


class TestConnectionGroup(unittest.TestCase):

    @run_async
    async def test_broadcast(self):
        group = create_group()
        message = dict(message='message')
        await group.broadcast(message)
        for client in group.clients:
            self.assertIn(message, client.socket.sent_messages)

    @run_async
    async def test_multicast(self):
        group = create_group()
        message = dict(message='message')
        emitter = group.clients[0]
        await group.multicast(emitter, message)
        for client in group.clients:
            if client == emitter:
                self.assertNotIn(message, client.socket.sent_messages)
            else:
                self.assertIn(message, client.socket.sent_messages)

    def test_group_has_size_property(self):
        group = create_group()

        def set_size():
            group.size = 0

        self.assertRaises(Exception, set_size)
        self.assertEqual(group.size, __default_size__)

    def test_get_connected_clients(self):
        group = create_group()
        connected_clients = group.get_connected_clients()
        for client in connected_clients:
            self.assertTrue(client.is_connected)
            client.socket.connected = False
        connected_clients = group.get_connected_clients()
        self.assertEqual(len(connected_clients), 0)

    def test_connection_group_is_iterable(self):
        group = create_group()
        counter = 0
        for _ in group:
            counter += 1
        self.assertEqual(counter, __default_size__)

    def test_back_reference_from_client_connection_to_connection_group(self):
        group = create_group()
        for client in group:
            self.assertEqual(client.group, group)

    def test_list_all_clients_but_one(self):
        group = create_group()
        one = group.clients[0]
        expected_others = group.clients[1:]
        others = group.but(one)

        self.assertNotIn(one, others)
        self.assertListEqual(others, expected_others)
