class User:

    def __init__(self,
                 name=None,
                 password=None,
                 token=None):

        self.name = name
        self.password = password
        self.token = token

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return other.name == self.name
