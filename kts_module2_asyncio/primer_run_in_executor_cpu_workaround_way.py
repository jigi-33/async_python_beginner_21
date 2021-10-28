"""
Обходной путь для CPU bound операций. Оригин. run_in_executor/cpu_workaround.py

Бизнес-логика такого обхода:

Чтобы работала кооперативная многозадачность, нужно чтобы контекст переключался
между короутинами. Это происходит в момент выполнения вызова async-функции
с синтаксисом await.
В случае с бесконечным while True циклом управление никогда не вернется в Evt.L
Это потому, что никогда не будет вызвана асинхронная функция.
Поэтому мы вызовем ее искусственно: Для этого вызовем await asyncio.sleep
со временем ожидания 0. Вызывать ее можно управляемо раз в N итераций цикла
(условие под if подбирается).
В итоге имеем:
1. cpu-операция будет тратить время процессора в классическом виде;
2. при этом будет периодически передаваться управление другим короутинам
для выполнения чего-им-там-нужно и вставать обратно в очередь event loop.
При таком подходе мы получим идентичный с ThreadPoolExecutor результат.
Только в этом случае уже не ОС решает, в какой момент отдать управление
eventLoop'у, а разработчик.
"""
import asyncio
import datetime


async def blocking_task_cpu_bound():
    counter = 50000000
    while counter > 0:
        counter -= 1
        if counter % 1000 == 0:     # \     The
            await asyncio.sleep(0)  # /  solution (workaround)


async def blocking_worker():
    while True:  # Если свободна
        await blocking_task_cpu_bound()


async def ticker():
    while True:  # Если свободна
        print(datetime.datetime.now())
        await asyncio.sleep(1)  # для проверки


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(ticker())
    loop.create_task(blocking_worker())

    loop.run_forever()  # такое завершение нужно всегда, если есть только Loop.
