import bcrypt
from time import time

from engine.repositories.user_repository import UserRepository


class Authentication:

    @staticmethod
    def _generate_token(name: str):
        timestamp = str(int(time()))
        token = name + ':' + timestamp
        token = token.encode()
        return bcrypt.hashpw(
            token,
            bcrypt.gensalt()
        )

    def __init__(self, users: UserRepository):
        self.users = users

    async def login(self, name: str, password: str) -> bool:
        if await self._authenticate_user(name, password):
            token = Authentication._generate_token(name)
            await self.users.set_token(name, token)
            return token
        return False

    async def logout(self, token: str) -> bool:
        return await self.users.delete_token(token)

    async def validate_token(self, token: str) -> bool:
        return await self.users.get_by_token(token) is not None

    async def _authenticate_user(self, name: str, password: str):
        user = await self.users.get_by_name(name)
        if user:
            password = password.encode()
            return bcrypt.checkpw(password, user.password)
        return False
