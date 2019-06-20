from engine.controllers.start_match import play_next_match

from engine.io.client_connection import ClientConnection

from engine.models.user import User

from engine.views.decorators import (
    require_auth_web_socket,
    extract_waiting_list,
    extract_game_loop
)


@extract_waiting_list
@extract_game_loop
@require_auth_web_socket
async def enter_waiting_list(request,
                             *args,
                             socket=None,
                             user=None,
                             waiting_list=None,
                             game_loop=None,
                             **kwargs
                             ):

    user_name = user[User.__name_attr__]
    client = ClientConnection(user_name, socket)
    ack = dict(
        message='you are now in the waiting list',
        status=200
    )
    await client.send(ack)
    await play_next_match(client, waiting_list, game_loop)
    return socket
