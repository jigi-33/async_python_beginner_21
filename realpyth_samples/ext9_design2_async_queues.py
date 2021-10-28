# originally asyncq.py from RealPython extended article.

import asyncio
import itertools as it
import os
import random
import time

"""
Async IO design patterns - using a Queues. (So smart-n-powerful Example!)

In this design, there is no chaining of any individual consumer to a producer
The consumers don’t know the number of producers, or even the cumulative number of items
that will be added to the queue. The queue serves as a throughput that can communicate with the
producers and consumers without them talking to each other directly.

In asynchronous version, the challenging part of this workflow is that there needs to be a _signal_
to the consumers that production is done. Otherwise, await q.get() will hang indefinitely
because the queue will have been fully processed, but consumers won’t have any idea
that production is complete

Использование асинхронной очереди в данном случае заключается в том, что она
действует лишь как способ передачи от производителей к потребителям, которые напрямую не связаны
или совсем не связаны друг с другом.

NOTE: We keeps in mind that asyncio.sleep() is used here to mimic some other, more complex coroutine
that would eat up time and block all other execution if it were a regular blocking function.
"""


async def makeitem(size: int = 5) -> str:
    return os.urandom(size).hex()  # equal to random.SystemRandom() - OS-resources based rnd numbers


async def randsleep(caller=None) -> None:
    i = random.randint(0, 10)
    if caller:
        print(f"{caller} sleeping for {i} seconds.")
    await asyncio.sleep(i)


async def produce(name: int, q: asyncio.Queue) -> None:
    n = random.randint(0, 10)
    for _ in it.repeat(None, n):  # Synchronous loop for each single producer
        await randsleep(caller=f"Producer {name}")
        i = await makeitem()
        t = time.perf_counter()
        await q.put((i, t)
                    )
        print(f"Producer {name} added <{i}> to queue.")


async def consume(name: int, q: asyncio.Queue) -> None:
    while True:
        await randsleep(caller=f"Consumer {name}")
        i, t = await q.get()
        now = time.perf_counter()
        print(f"Consumer {name} got element <{i}>"
              f" in {now-t:0.5f} seconds.")
        q.task_done()


async def main(nprod: int, ncons: int):
    q = asyncio.Queue()
    producers = [asyncio.create_task(produce(n, q)) for n in range(nprod)
                 ]
    consumers = [asyncio.create_task(consume(n, q)) for n in range(ncons)
                 ]
    await asyncio.gather(*producers)
    await q.join()  # Implicitly awaits consumers, too, but...
    for c in consumers:  # в конце нужно будет оменить все потребителькие задачки, т.к. в ином случ.
        c.cancel()       # зависли бы в бесконечности!


if __name__ == "__main__":
    """
    When a consumer pulls an item out, it simply calculates the elapsed time that the item sat
    in the queue using the timestamp that the item was put in with.
    """
    import argparse

    random.seed(444)

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--nprod", type=int, default=5)  # number of coro-producers
    parser.add_argument("-c", "--ncons", type=int, default=10)  # number of cunsumers
    ns = parser.parse_args()

    start = time.perf_counter()
    asyncio.run(main(**ns.__dict__))  # выкрутасно, но в целом ясно
    elapsed = time.perf_counter() - start

    print(f"\nProgram completed in {elapsed:0.5f} secs\n")
