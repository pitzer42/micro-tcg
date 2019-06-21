from engine import routes
from engine.io.gamepad import Gamepad
from engine.models.user import User


class TestGamepad(Gamepad):

    async def get_all_users(self):
        url = self.base_url + routes.users
        return await self.session.get(url)

    async def login(self, expect_success=True):
        url = self.base_url + routes.login
        doc = self.user.__dict__
        response = await self.session.get(
            url,
            json=doc
        )
        if expect_success:
            response_json = await response.json()
            self.user.token = response_json[User.__token_attr__]
        return response

    async def login_with_wrong_name(self):
        bkp = self.user.name
        self.user.name += 'wrong'
        response = await self.login(expect_success=False)
        self.user.name = bkp
        return response

    async def login_with_wrong_password(self):
        bkp = self.user.password
        self.user.password += 'wrong'
        response = await self.login(expect_success=False)
        self.user.password = bkp
        return response
