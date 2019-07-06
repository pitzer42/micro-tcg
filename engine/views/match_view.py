from engine.controllers.start_match import play_next_match

from engine.io.client_connection import ClientConnection

from engine.models.user import User

from engine.views.decorators import (
    require_auth,
    require_waiting_list,
    require_game_loop,
    web_socket_view
)


@web_socket_view
@require_waiting_list
@require_game_loop
@require_auth
async def enter_waiting_list(request,
                             *args,
                             socket=None,
                             user=None,
                             waiting_list=None,
                             game_loop=None,
                             **kwargs
                             ):
    try:
        user_name = user[User.__name_attr__]
        client = ClientConnection(user_name, socket)
        ack = dict(
            message='you are now in the waiting list',
            status=200
        )
        await client.send(ack)
        await play_next_match(client, waiting_list, game_loop)
    except IOError as e:
        print(e)
    return socket
