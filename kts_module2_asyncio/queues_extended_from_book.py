import asyncio
import logging

logging.basicConfig(level=logging.DEBUG)


# расширенный навороченный пример с очередью(asyncio.Queue) и Event-синхронизатором.
# прикручено логирование в stdout.

async def producer(iterable, queue: asyncio.Queue, shutd_evt: asyncio.Event):
    for i in iterable:
        if shutd_evt.is_set():  # когда продьюсер наработался, будет завершаться
            break
        try:
            queue.put_nowait(i)
            await asyncio.sleep(0)
        except asyncio.QueueFull as err:
            logging.warning("The queue is too full,Maybe worker are too slow.")
            raise err
    shutd_evt.set()


async def worker(name, handler, queue: asyncio.Queue, shutd_evt: asyncio.Event):
    while not shutd_evt.is_set() or not queue.empty():  # GP! как в коде асинхронного краулера от AO/kts
        try:
            work = queue.get_nowait()
            # Simulate some work
            handler(await asyncio.sleep(1.0, work))
            logging.debug(f"worker {name}: {work}")
        except asyncio.QueueEmpty:   # если не использовать join(), прикрываемся обработчиком исключения
            await asyncio.sleep(0)


async def main():
    n, handler, iterable = 10, lambda val: None, [i for i in range(500)]

    shutd_evt = asyncio.Event()
    queue = asyncio.Queue()

    worker_coros = [worker(
        f"worker_{i}", handler, queue, shutd_evt) for i in range(n)]

    producer_coro = producer(iterable, queue, shutd_evt)

    coro = asyncio.gather(
        producer_coro,
        *worker_coros,
        return_exceptions=True
    )

    try:
        await coro
    except KeyboardInterrupt:
        shutd_evt.set()
        coro.cancel()


if __name__ == '__main__':
    """
    Программа будет работать в замкнутом цикле, пока не прервем по ctrl-c
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Pressed ctrl+c...")
