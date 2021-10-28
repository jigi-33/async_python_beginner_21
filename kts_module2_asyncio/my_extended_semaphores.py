import asyncio
from asyncio.exceptions import CancelledError
import concurrent.futures


# pytestmark = pytest.mark.asyncio

counter = 0

# TODO используя Semaphore избежать длительного сна


def close_futures():
    _, pending = concurrent.futures.wait(
        asyncio.all_tasks(), timeout=0.1,
        return_when=concurrent.futures.FIRST_EXCEPTION,
        )
    for p in pending:
        if isinstance(p, asyncio.Future):
            p.cancel()


async def do_request():
    global counter
    sem = asyncio.Semaphore(value=5)
    try:
        async with sem:
            counter += 1
            print(counter)
            if counter > 5:
                await asyncio.sleep(10)
            await asyncio.sleep(0.1)
            counter -= 1
    except CancelledError:
        await close_futures()
        try:
            loop.stop()
        except RuntimeError:
            pass


async def main():
    await asyncio.wait_for(
        asyncio.gather(*[do_request() for _ in range(10)]),
        timeout=1.2,
    )


loop = asyncio.get_event_loop()
# try:
loop.run_until_complete(main())
# except RuntimeError as err:
#     print(err)
loop.close()
