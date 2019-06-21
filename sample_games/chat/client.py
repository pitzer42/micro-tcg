import asyncio

from aiohttp import ClientSession

from engine.io.gamepad import Gamepad


if __name__ == '__main__':

    async def connect_gamepad():
        gamepad = Gamepad(
            session=ClientSession()
        )
        gamepad.base_url = 'http://localhost:8080'
        await gamepad.start()
        await gamepad.receive_and_send_loop()

    asyncio.run(connect_gamepad())
