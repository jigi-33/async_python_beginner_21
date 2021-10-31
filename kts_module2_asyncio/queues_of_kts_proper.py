import asyncio

"""
Небольшая вариация примера про Queues из материалов lms KTS.
(изначально в логике скрипта была мелкая ошибка, потом её поправили)
"""


async def vk_request(queue):
    await asyncio.sleep(1.5)
    print("performing request...done!\n")
    return [{'key1': 'value1'},
            {'key2': 'value2'},
            ]


async def sender_worker(queue):
    while True:
        events: list[dict] = await vk_request(queue)
        for e in events:
            await queue.put(e)


async def reader_worker(queue):
    while True:
        data = await queue.get()  # достанет все имеющиеся данные из буфера очереди
        print(data)


async def main():
    tasks = []
    reader_workers_count = 10
    queue = asyncio.Queue()
    task = asyncio.create_task(sender_worker(queue))
    tasks.append(task)

    for _ in range(reader_workers_count):
        task = asyncio.create_task(reader_worker(queue))
        tasks.append(task)

    await asyncio.gather(*tasks)


# (будет работать в замкнутом цикле, тк логика завершения по опустошению очереди здесь не расписана).
asyncio.run(main())
