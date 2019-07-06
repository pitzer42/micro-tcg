import asyncio


def run_async(f):
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        future = f(*args, **kwargs)
        if loop.is_running():
            return loop.create_task(future)
        else:
            return loop.run_until_complete(future)
    return wrapper
