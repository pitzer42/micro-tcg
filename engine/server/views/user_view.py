from aiohttp import web

from aiohttp_cors import CorsViewMixin

from engine.repositories.data_ports import dict_to_password_hashed_dict
from engine.repositories.user_repository import UserRepository

import engine.server.app_schema as app_schema
from engine.server.views.data_ports import user_to_secure_json_serializable_dict


class UserView(web.View, CorsViewMixin):

    __route__ = '/users'

    @property
    def users(self) -> UserRepository:
        return self.request.app[app_schema.user_repo]

    async def get(self):
        users_list = await self.users.to_list(
            data_port=user_to_secure_json_serializable_dict
        )
        return web.json_response(users_list)

    async def put(self):
        json_request = await self.request.json()
        command_result = await self.users.insert(
            json_request,
            data_port=dict_to_password_hashed_dict
        )
        return web.json_response(
            dict(
                inserted_id=str(command_result.inserted_id)
            )
        )