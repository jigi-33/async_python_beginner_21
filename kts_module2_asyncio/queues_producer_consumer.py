import asyncio
import random
import time


async def producer(shop_queue):
    while True:
        await asyncio.sleep(1)
        print("Putting an ice-cream item onto queue")
        await shop_queue.put(random.randint(1, 5))


async def customer(id, shop_queue):
    print(shop_queue)
    while True:
        print("Customer ID{} Attempting to get from queue...".format(id))
        item = await shop_queue.get()  # using get() withowt args
        if item is None:
            # the producer emits None to indicate that it is done!
            break
        print("Customer ID{} received ice-cream with id: {}".format(id, item))


def main():
    loop = asyncio.get_event_loop()
    shop_queue = asyncio.Queue(loop=loop, maxsize=10)  # очередь не вместит больше 10 человечков
    try:
        loop.run_until_complete(asyncio.gather(
            producer(shop_queue),
            customer(1, shop_queue),
            customer(2, shop_queue)
        )
        )
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()


if __name__ == '__main__':
    main()
