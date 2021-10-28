import asyncio
import time

SUB_PROGS_COUNT = 100


async def worker():
    await asyncio.sleep(0.5)


async def main():
    begin = time.time()
    await asyncio.gather(
        *[worker() for _ in range(SUB_PROGS_COUNT)]
    )
    print(time.time() - begin)

asyncio.run(
    main()
    )
