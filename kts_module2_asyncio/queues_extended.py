import asyncio
import random
import time


async def worker(name, queue):
    while True:  # если про очереди, то при воркере всегда начинать с while true
        # Получаем "рабочую единицу" данных, которые выходят из очереди.
        sleep_for = await queue.get()  # внутри воркера _данные_ достаются из очереди

        # Sleep for the "sleep_for" seconds (эмулятор полезной работы)
        await asyncio.sleep(sleep_for)

        # Уведомить очередь что текущая рабочая "work item" has been processed.
        queue.task_done()

        print(f'{name} has slept for {sleep_for:.2f} seconds')


async def main():
    # Создаем очередь, которая используется для загрузки ворклоада/пула активными задачами.
    queue = asyncio.Queue()

    # Generate random timings (our data) and put() them into the queue
    total_sleep_time = 0
    for _ in range(20):
        sleep_for = random.uniform(0.05, 1.0)  # формирование _данных_ для складывания их в очередь с put
        total_sleep_time += sleep_for
        queue.put_nowait(sleep_for)  # в большинстве случаев nowait использ. не треба - лишь обычный put

    # Создаем три рабочие Таски для кооперативно-многозадачно обработки в нашей очереди
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)

    # waiting until the queue is fully processed
    started_at = time.monotonic()
    await queue.join()   # join() будет ждать, пока очередь не станет абсолютно пустой
    total_slept_for = time.monotonic() - started_at

    # Здесь gather() и wait() не используется, т.к. используется join() и по бизнес логике,
    # задачи в конце отменяются.

    # Отменить (очистить) наши рабочие таски после опустошения очереди (по завершению 1 цикла)
    for task in tasks:
        task.cancel()

    print('====')
    print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
    print(f'total expected sleep time: {total_sleep_time:.2f} seconds')


asyncio.run(main())
