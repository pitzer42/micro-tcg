from engine.models.user import User

_i = 0


def create(i: int = None) -> User:
    global _i
    if i is None:
        i = _i
        _i += 1
    i = str(i)
    return User(
        name=f'name_{i}',
        password=f'password_{i}',
        token=f'token_{i}'
    )
