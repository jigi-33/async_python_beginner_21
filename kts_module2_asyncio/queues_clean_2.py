import asyncio
from codetiming import Timer


"""
У меня такой пример уже был.
"""


async def task(name, work_queue):
    timer = Timer(text=f"Task {name} elapsed time: {{:.1f}}")
    while not work_queue.empty():
        delay = await work_queue.get()
        print(f"Task {name} running")
        timer.start()
        await asyncio.sleep(delay)
        timer.stop()


async def main():
    """
    Это главная точка входа для главной программы
    """
    # Создание очереди работы
    work_queue = asyncio.Queue()

    # Помещение работы в очередь
    for work in [15, 10, 5, 2]:
        await work_queue.put(work)

    # Запуск задач при помощи контекста Таймера:
    with Timer(text="\nTotal elapsed time: {:.1f}"):
        await asyncio.gather(
            asyncio.create_task(task("One", work_queue)),
            asyncio.create_task(task("Two", work_queue)),
        )


if __name__ == "__main__":
    asyncio.run(main())