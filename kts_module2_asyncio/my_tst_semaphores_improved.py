import asyncio
from asyncio.exceptions import CancelledError
# import pytest

# pytestmark = pytest.mark.asyncio


# SOLVED !
#
# the_task_cond - используя Semaphore избежать длительного сна


async def do_request():
    global counter, sem
    if sem is None:
        sem = asyncio.Semaphore(5)
    async with sem:
        counter += 1
        print(counter)  # COMON DEBUG
        if counter > 5:
            await asyncio.sleep(10)
        await asyncio.sleep(0.1)
        counter -= 1


async def test():
    sem = asyncio.Semaphore(5)  # пришлось поправить её
    await asyncio.wait_for(
        asyncio.gather(*[do_request() for _ in range(10)]),
        timeout=1.2,
    )

counter = 0
sem = None


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(test())
    except RuntimeError as err:
        print(err)
    finally:
        loop.close()
