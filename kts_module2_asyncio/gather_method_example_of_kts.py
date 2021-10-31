import asyncio

"""
asyncio.gather() method example from KTS co-founder, Alexandr Opryshko.

"Gather" по природе тоже корутина, поэтому ее всегда нужно вызывать с await;
Главная идея - собрать все таски (обозначенные явным образом), либо корутины (2й случай), и кинуть
в gather, а он, дождавшись их завершения, вернет результат выполнения в виде списка завершенных.
"""

async def worker():
    while True:
        print("I'm a worker")
        await asyncio.sleep(1)


async def runner_1():
    """ вариант с Тасками """
    task1 = asyncio.create_task(worker())
    task2 = asyncio.create_task(worker())
    await asyncio.sleep(4)
    print("await asyncio.sleep(4) reached")
    await asyncio.gather(task1, task2)


async def runner_2():
    """ вариант с 'исходными' корутинами """
    quasi_task1 = worker()
    quasi_task2 = worker()
    await asyncio.sleep(3)
    print("await asyncio.sleep(3) reached")

    # Итоги обоих раннеров по законченному действию тождественны.
    await asyncio.gather(quasi_task1, quasi_task2)


asyncio.get_event_loop().run_until_complete(
            runner_2()
            )
