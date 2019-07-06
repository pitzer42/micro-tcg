from engine.repos.users import Users


class Repositories:

    def __init__(self):
        self._users: Users = None

    @property
    def users(self) -> Users:
        return self._users
