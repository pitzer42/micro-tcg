import asyncio

_loop = None


def sync(coroutine):

    def wrapper(*args, **kwargs):
        global _loop

        if _loop is None:
            _loop = asyncio.new_event_loop()
            asyncio.set_event_loop(_loop)

        future = coroutine(*args, **kwargs)
        try:
            _loop.run_until_complete(future)
        except RuntimeError:
            future = coroutine(*args, **kwargs)
            asyncio.run_coroutine_threadsafe(future, _loop)

    return wrapper