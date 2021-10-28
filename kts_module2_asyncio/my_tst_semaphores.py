import asyncio
# import pytest

# pytestmark = pytest.mark.asyncio
# TODO используя Semaphore избежать длительного сна не более 5 экз-ров


async def do_request(num, sem):
    global counter
    async with sem:
        print(f'starting request {num+1}')
        counter += 1
        print(counter)
        if counter > 5:
            await asyncio.sleep(10)
        await asyncio.sleep(0.1)
        counter -= 1


async def main():
    sem = asyncio.Semaphore(value=5)
    await asyncio.wait_for(
        asyncio.gather(*[do_request(i, sem) for i in range(10)]),
        timeout=1.2,
    )


if __name__ == '__main__':
    counter = 0
    # sem = None
    asyncio.run(main())
