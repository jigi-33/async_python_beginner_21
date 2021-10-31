import asyncio
from dataclasses import dataclass
from typing import Optional
from yarl import URL
from task import Task
from fetch_task import FetchTask
#
# На поверку работает не очень корректно: клиент aiohttp выкидывает исключение "too many redirects" :(
#

rate_limit = 5   # доп. лимитёр кол-ва задач, пропускаемых пулом


class Pool:  # управляет кол-вом запросов в единицу времени; принимает на входе 3 параметра
    def __init__(
        self, max_rate: int, interval: int = 1,
        concurrent_level: Optional[int] = None,  # кол-во параллельных запросов при его ограничении
    ):
        self.max_rate = max_rate
        self.interval = interval
        self.concurrent_level = concurrent_level
        self.is_running = False
        self._queue = asyncio.Queue()
        self._sheduler_task: Optional(asyncio.Task) = None
        self._sem = asyncio.Semaphore(concurrent_level or max_rate)  # ограничель кол-ва || кор 1 назнач
        self._concurrent_workers = 0
        self._stop_event = asyncio.Event()  # событие для возобновления работы шедалера

    async def _worker(self, task: Task):  # простой исполнитель задачки класса Task
        async with self._sem:
            self._concurrent_workers += 1  # особенность записи внутри семафоров (good practice)
            await task.perform(self)
            self._queue.task_done()  # std method indicates that task is complete:для красоты оформления
        self._concurrent_workers -= 1  # особенность записи внутри семафоров (good practice)
        if not self.is_running and self._concurrent_workers == 0:
            self._stop_event.set()  # асинхронное событие наступило и уведомление об этом поймает stop()

    async def _sheduler(self):  # работает постоянно
        while self.is_running:
            for _ in range(self.max_rate):
                async with self._sem:
                    task = await self._queue.get()  # достать задачу из очереди а не создавать напрямую
                    asyncio.create_task(self._worker(task))
            await asyncio.sleep(self.interval)   # сколько шедалер спит между запросами

    def start_schd(self):  # запускает фоновый планировщик, этот лаунчер не обязан быть асинхронным
        self.is_running = True
        self._sheduler_task = asyncio.create_task(self._sheduler())

    async def put(self, task: Task):
        await self._queue.put(task)

    async def join(self):
        await self._queue.join()  # join - будет ждать, пока очередь не станет абсолютно пустой

    async def stop(self):
        self.is_running = False
        self._sheduler_task.cancel()   # отменит задачу планировщика
        if self._concurrent_workers != 0:
            await self._stop_event.wait()  # ждём события о реальной готовности к стопарению


async def start(pool):
    await pool.put(
        FetchTask(
            tid=1,
            url=URL('https://habr.com/ru/company/kts/blog/'),
            depth=1,
        )
    )
    pool.start_schd()
    await pool.join()
    await pool.stop()

def main():
    loop = asyncio.get_event_loop()
    pool = Pool(3)  # 3 запроса в секунду

    try:
        loop.run_until_complete(start(pool))
    except KeyboardInterrupt:
        loop.run_until_complete(pool.stop())  # пул завершает работу лишь по ctr-c, потом прикрываем луп
        loop.close()


if __name__ == '__main__':
    main()
