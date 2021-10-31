import asyncio
from codetiming import Timer

"""
такой пример по Queues уже был, но здесь лучше прокомментировано.
"""


async def task(name, work_queue):
    timer = Timer(text=f"Task {name} elapsed time: {{:.1f}}")
    while not work_queue.empty():
        delay = await work_queue.get()  # взять _данные_ из очереди - уже без аргумента(!)
        print(f"Task {name} running")
        timer.start()
        await asyncio.sleep(delay)
        timer.stop()


async def main():
    """
    функция main - по канонам основная точка входа в асинхронную программу
    """
    # создаем очередь задач(тасок)
    work_queue = asyncio.Queue()

    # помещаем в очередь _данные_
    for work in [15, 10, 5, 2]:
        await work_queue.put(work)  # положить _данные_ в очередь

    # помещаем & запускаем таски при помощи контекста Таймера, нужного для корректного замера времени.
    with Timer(text="\nTotal elapsed time: {:.1f}"):
        await asyncio.gather(
            asyncio.create_task(task("One", work_queue)),
            asyncio.create_task(task("Two", work_queue)),
        )


if __name__ == "__main__":
    asyncio.run(main())
