import asyncio

"""
Пример очередей из материалов Kts.
Логика до конца не расписана поэтому как работает, неочевидно.
"""


async def vk_request(q):
    q = asyncio.Queue()
    await asyncio.sleep(1.5)
    print("performing request...done!\n")
    return [{'key1': 'value1'},
            {'key2': 'value2'},
            ]


async def sender_worker(queue):
    while True:
        events: list[dict] = await vk_request()
        for e in events:
            await queue.put()


async def reader_worker(queue):
    while True:
        data = await queue.get()
        # some logic
        pass


async def main():
    tasks = []
    reader_workers_count = 10
    queue = asyncio.Queue()
    task = asyncio.create_task(vk_request(queue))
    tasks.append(task)

    for _ in range(reader_workers_count):
        task = asyncio.create_task(reader_worker(queue))
        tasks.append(task)

    await asyncio.gather(*tasks)


asyncio.run(main())
