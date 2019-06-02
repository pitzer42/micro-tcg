from aiohttp import WSMsgType
from micro_tcg.views.decorators import require_auth_web_socket


class Match:

    waiting_list = dict()

    @staticmethod
    async def make_match():
        # enough players for at least one match
        while len(Match.waiting_list) > 1:

            # two items make a match
            token_a, socket_a = Match.waiting_list.popitem()
            token_b, socket_b = Match.waiting_list.popitem()
            try:
                match_a = dict(opponent=token_b)
                match_b = dict(opponent=token_a)
                if socket_a.closed or socket_b.closed:
                    raise IOError
                await socket_a.send_json(match_a)
                await socket_b.send_json(match_b)
            except IOError:

                # something went wrong, keep the items that still active and continue
                if not socket_a.closed:
                    Match.waiting_list[token_a] = socket_a
                if not socket_b.closed:
                    Match.waiting_list[token_b] = socket_b


@require_auth_web_socket
async def enter_waiting_list(socket, user):
    ack_json = dict(
        message='you are now in the waiting list'
    )
    await socket.send_json(ack_json)
    Match.waiting_list[user.username] = socket

    await Match.make_match()

    async for message in socket:
        if message.type == WSMsgType.TEXT:
            if message.data == 'close':
                await socket.close()
            else:
                print(message)
        elif message.type == WSMsgType.ERROR:
            print('%s connection closed with exception %s' % (
                user.username,
                socket.exception()
            ))

    return socket
