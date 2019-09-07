import asyncio

_loop = None


def sync(coroutine):

    def wrapper(*args, **kwargs):
        global _loop
        if _loop is None:
            _loop = asyncio.new_event_loop()
        future = coroutine(*args, **kwargs)
        _loop.run_until_complete(future)

    return wrapper