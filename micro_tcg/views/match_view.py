from micro_tcg.io.user_io import ClientConnection

from micro_tcg.models.user import User

from micro_tcg.views.decorators import (
    require_auth_web_socket,
    inject_waiting_list
)


@inject_waiting_list
@require_auth_web_socket
async def enter_waiting_list(request, *args, socket=None, user=None, waiting_list=None, **kwargs):
    user_name = user[User.__name_attr__]
    client = ClientConnection(user_name, socket)
    ack = dict(
        message='you are now in the waiting list',
        status=200
    )
    await client.send(ack)

    waiting_list.add(client)
    await waiting_list.next_match.wait()
    await waiting_list.match.start(client)

    return socket
