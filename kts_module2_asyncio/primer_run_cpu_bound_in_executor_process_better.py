"""
CPU bound операции. Оригинальный скрипт run_in_executor/cpu.py.

Лучше делать через ProcessPoolExecutor, т.к. запускается отдельный процесс,
а межпроцессное взаимодействие работает через sockets, тут нет потери производ.

В случае с Тред-экзекутором, CPU-bound операция будет _отнимать_ процессорное
время у EventLoop. При этом ОС принимает решение, в какой момент включить один
или другой тред. Т-же добавляются накладные расходы на переключение между ними.
"""
import asyncio
import concurrent.futures
import datetime


def blocking_task_cpu_bound_operation():  # Blocking CPU-bound operation
    counter = 50000000
    while counter > 0:
        counter -= 1


async def blocking_worker():
    while True:  # если свободна
        blocking_task_cpu_bound_operation()


async def async_thread_worker():  # Non-Optimal way
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor(2) as pool:
        while True:
            await loop.run_in_executor(pool, blocking_task_cpu_bound_operation)


async def async_process_worker():  # Optimal solution!
    loop = asyncio.get_running_loop()
    with concurrent.futures.ProcessPoolExecutor(2) as pool:
        while True:
            await loop.run_in_executor(pool, blocking_task_cpu_bound_operation)


async def ticker():
    while True:
        print(datetime.datetime.now())
        await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(ticker())
    # loop.create_task(blocking_worker())  # BAD way - will be block EventLoop
    # loop.create_task(async_thread_worker())  # Worse way.

    loop.create_task(async_process_worker())  # Optimal for CPU-bnd operations.

    loop.run_forever()  # в сл. если только Loop-инстанс, всегда в конце циклим
