import asyncio
import logging

logging.basicConfig(level=logging.DEBUG)


async def producer(iterable, queue: asyncio.Queue, shutdevt: asyncio.Event):
    for i in iterable:
        if shutdevt.is_set():
            break
        try:
            queue.put_nowait(i)
            await asyncio.sleep(0)
        except asyncio.QueueFull as err:
            logging.warning("The queue is too full,Maybe worker are too slow.")
            raise err
    shutdevt.set()


async def worker(name, handler, queue: asyncio.Queue, shutdevt: asyncio.Event):
    while not shutdevt.is_set() or not queue.empty():
        try:
            work = queue.get_nowait()
            # Simulate work
            handler(await asyncio.sleep(1.0, work))
            logging.debug(f"worker {name}: {work}")
        except asyncio.QueueEmpty:
            await asyncio.sleep(0)


async def main():
    n, handler, iterable = 10, lambda val: None, [i for i in range(500)]
    shutdevt = asyncio.Event()
    queue = asyncio.Queue()

    worker_coros = [worker(
        f"worker_{i}", handler, queue, shutdevt) for i in range(n)]

    producer_coro = producer(iterable, queue, shutdevt)

    coro = asyncio.gather(
        producer_coro,
        *worker_coros,
        return_exceptions=True
    )

    try:
        await coro
    except KeyboardInterrupt:
        shutdevt.set()
        coro.cancel()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # It bubbles up
        logging.info("Pressed ctrl+c...")
