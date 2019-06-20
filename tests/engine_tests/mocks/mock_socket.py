class SocketMock:

    def __init__(self):
        self.closed = False
        self.sent_messages = list()
        self.received_messages = list()

    async def send_json(self, json):
        self.sent_messages.append(json)

    async def receive_json(self):
        return self.received_messages.pop()
