"""
Another good Queue's "producer-consumer" example.

Adding items to Queues with put() or removing items with get()
are both _asynchronous_ operations,
since the queue size might be fixed (blocking an addition)
or the queue might be empty (blocking a call to fetch an item)
"""

import asyncio


async def consumer_receiver(n, q):
    print('consumer {}: starting'.format(n))
    while True:                            # use this feature on worker's starting with Queues !
        print('consumer {}: waiting for item'.format(n))
        item = await q.get()
        print('consumer {}: has item {}'.format(n, item))
        if item is None:
            # None is the signal to stop.
            q.task_done()
            break
        else:
            await asyncio.sleep(0.01 * item)
            q.task_done()
    print('consumer {}: ending'.format(n))


async def producer_sender(q, num_workers):
    print('producer: starting')
    # Add some numbers(aka DATA) to the queue to simulate jobs
    for i in range(num_workers * 3):
        await q.put(i)
        print('producer: added task {} to the queue'.format(i))

    # A FEATURE: add None entries in the queue to signal the receivers to exit!
    print('producer: adding stop signals to the queue')
    for i in range(num_workers):
        await q.put(None)
    print('producer: waiting for queue to empty...')
    await q.join()  # the main worker waits for queue is empty
    print('producer: ending!')


async def main(loop, num_consumers):
    # Create the queue with a fixed size so the producer
    # will block until the consumers pull some items out
    q = asyncio.Queue(maxsize=num_consumers)

    # Scheduled the consumer tasks with this way:
    consumers = [
        loop.create_task(consumer_receiver(i, q))
        for i in range(num_consumers)
    ]

    # Schedule the producer task in _separate_ line:
    prod = loop.create_task(producer_sender(q, num_consumers))

    # Wait for all-the-coroutines to finish
    await asyncio.wait(consumers + [prod])  # odd argument syntax(!)


if __name__ == '__main__':
    """
    Scenario/loop with ending with None-statement in 'producer' coro
    """
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(event_loop, 2))
    finally:
        event_loop.close()
