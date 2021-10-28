# asyncio_coroutine.py
import asyncio


async def coroutine():
    print('-== inside a coroutine ==-')


event_loop = asyncio.get_event_loop()

try:
    print('starting coroutine...')
    coro = coroutine()
    print('Entering EventLoop...')
    event_loop.run_until_complete(coro)

finally:
    print('closing event loop...')
    event_loop.close()
    print('closed!')
