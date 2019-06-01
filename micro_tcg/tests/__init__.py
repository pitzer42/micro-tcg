import asyncio


def sync(f):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        future = f(*args, **kwargs)
        return loop.run_until_complete(future)
    return wrapper
