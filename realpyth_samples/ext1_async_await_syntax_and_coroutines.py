import asyncio

"""
Coroutine - a function that can suspend its execution before reaching return
and it can indirectly pass control to another coroutine for some time.

countasync.py in original article - http://realpython.com/async-io-python
"""


async def count():  # the native courutine
    print("One")
    await asyncio.sleep(5)  # asyncio has own sleep replacement of time.sleep, use it with asyncio!
    print("Two")


async def main():  # main code block
    await asyncio.gather(   # starts a group of courutine functions
        count(),   # the order of this output is the heart of async IO.
        count(),   # talking to each of the calls of count() is a single event loop, or Coordinator.
        count()
    )


if __name__ == "__main__":
    import time
    s = time.perf_counter()

    asyncio.run(main())  # the specific execution of whole async program

    elapsed = time.perf_counter() - s  # calculate execution time

    print(f"{__file__} executed in {elapsed:0.2f} seconds\n")
