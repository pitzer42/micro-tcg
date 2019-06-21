import unittest

from tests.engine_tests import run_async
from tests.engine_tests.mocks.mock_socket import SocketMock

from engine.io.client_connection import ClientConnection


class TestClientConnection(unittest.TestCase):

    def test_equality_defined_by_id(self):
        class Dummy(object):
            def __init__(self, _id):
                self._id = _id

        id_a = 'a'
        id_b = 'b'
        socket_a = SocketMock()
        socket_b = SocketMock()

        client_a = ClientConnection(id_a, socket_a)
        client_b = ClientConnection(id_b, socket_b)
        client_c = ClientConnection(id_a, socket_b)
        dummy = Dummy(id_a)

        self.assertEqual(client_a, client_c)
        self.assertNotEqual(client_b, client_c)
        self.assertNotEqual(client_a, dummy)

    @run_async
    async def test_send(self):
        message = dict(message='message')
        socket = SocketMock()
        client = ClientConnection(None, socket)
        await client.send(message)

        self.assertIn(message, socket.sent_messages)

    @run_async
    async def test_receive(self):
        message = dict(message='message')
        socket = SocketMock()
        socket.received_messages.append(message)
        client = ClientConnection(None, socket)
        received_message = await client.receive()

        self.assertEqual(message, received_message)

    def test_raises_exception_when_trying_to_send_message_with_closed_socket(self):
        @run_async
        async def invoke_send():
            return await client.send(message)

        socket = SocketMock()
        socket.closed = True
        client = ClientConnection(None, socket)
        message = dict()

        self.assertRaises(IOError, invoke_send)

    def test_is_closed_retrieves_socket_state(self):
        socket = SocketMock()
        client = ClientConnection(None, socket)

        socket.closed = True
        self.assertTrue(client.is_connected)

        socket.closed = False
        self.assertFalse(client.is_connected)
