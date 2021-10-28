"""
IO bound операции. В оригинале предлагается run_in_executor/io.py
"""
import asyncio
import concurrent.futures
import datetime
import requests


def blocking_task():  # синхронная блокирующая операция
    requests.get('https://docs.python.org/3/')


async def blocking_worker():
    while True:
        blocking_task()


async def async_thread_worker():
    # loop = asyncio.get_event_loop()
    loop = asyncio.get_running_loop()   # в корутине лучше использ вместо g_e_l

    with concurrent.futures.ThreadPoolExecutor(2) as pool:
        while True:
            await loop.run_in_executor(pool, blocking_task)


async def ticker():
    while True:
        print(datetime.datetime.now())
        await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop = asyncio.get_running_loop()  # вне корутин использовать r_g_l низзя
    loop.create_task(ticker())
    # loop.create_task(blocking_worker()) #-blocking_worker заблокирует EvtLoop
    loop.create_task(async_thread_worker())  # а это верный подход, все воркает

    loop.run_forever()  # зацикливаем сам луп
