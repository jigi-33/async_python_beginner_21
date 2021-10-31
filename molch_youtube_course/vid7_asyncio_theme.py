# Видео 7 курса "Асинхронность" - начало.

# синтаксис async/await на замену @asyncio.coroutine и yield from
# пример асинхронного скачивания файлов.

# в модуле asyncio в событийном цикле крутятся экземпляры класса Task / Future
# которые по сути является контейнерами для корутин.

# Task - подкласс класса Future. Фьюча - это результат работы асинхронной программы в будущем.
# в джаваскрипте эта сущность называется Promise (обещание)
# с классом Task ассоциируются корутины

# asyncio поставляет высокий уровень абстракции касаемо событийного цикла и инкапсуляции корутин
# в класс Task

# Лучший пример асинхронности - от Олега.
# Две самостоятельные функции, одна будет производить числа от 0 до бескон, а другая будет
# сообщать какое-нить сообщение, в нашем случае - время.

import os             # ДЛЯ ASYNC ОТЛАДКИ
import asyncio
from time import time
import logging        # ДЛЯ ASYNC ОТЛАДКИ
import warnings       # ДЛЯ ASYNC ОТЛАДКИ

os.environ['PYTHONASYNCIODEBUG'] = '1'    # ДЛЯ ASYNC ОТЛАДКИ

logging.basicConfig(level=logging.DEBUG)  # ДЛЯ ASYNC ОТЛАДКИ
logging.getLogger("asyncio").setLevel(logging.DEBUG)   # ДЛЯ ASYNC ОТЛАДКИ

warnings.resetwarnings()  # ДЛЯ ASYNC ОТЛАДКИ


# @asyncio.coroutine  # из обычной ф-и создает корутину, основанную на генераторах (старый синтаксис)
async def print_numbers():
    num = 1
    while True:
        print(num)
        await asyncio.sleep(0.5)  # асинхронный sleep
        num += 1


async def print_time():
    count = 0
    while True:  # бесконечный цикл
        if count % 3 == 0:
            print(f"{count} seconds have passed")
        count += 1
        await asyncio.sleep(1)


async def main():
    task1 = asyncio.create_task(print_numbers())  # создаем таски (новый синтаксис)
    task2 = asyncio.create_task(print_time())

    await asyncio.gather(task1, task2)


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(
    #     main()
    # )
    # loop.close()
    asyncio.run(    # новый синтаксис
        main(),
        debug=True,  # УКАЗЫВАЕМ ПРИ ОТЛАДКЕ
    )
