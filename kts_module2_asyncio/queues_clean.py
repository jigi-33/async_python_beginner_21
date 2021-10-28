import asyncio

""" Queue 'clean' example from lms content """


async def vk_request(queue):
    while True:
        for i in range(100):
            print("do request")
        break


async def sender_worker(queue):
    while True:
        events: list[dict] = await vk_request()
        for e in events:
            await queue.put()  # положить в очередь


async def reader_worker(queue):
    while True:
        data = await queue.get()   # достать из очереди
        print('Reading...')
        await asyncio.sleep(2)
        print('Done!')


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
