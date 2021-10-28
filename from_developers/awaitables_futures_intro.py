import asyncio
import concurrent.futures

"""
A Future is a special low-level awaitable object that represents an eventual result of an asynchronous operation.
When a Future object is awaited - it means that the coroutine will wait until the Future is resolved in some other place.
Future objects in asyncio are needed to allow _callback-based_ code to be used with async/await.
Normally there is NO need to create Future objects at the application level code.

async def main():
    await function_that_returns_a_future_object()

    # this is also valid:
    await asyncio.gather(
        function_that_returns_a_future_object(),
        some_python_coroutine()
    )

"""


def blocking_io():
    # File operations (such as logging) can block the event loop: run them in a thread pool
    with open('/dev/urandom', 'rb') as f:
        return f.read(100)


def cpu_bound():
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a process pool.
    return sum(i * i for i in range(10 ** 7))


async def main():
    loop = asyncio.get_running_loop()

    # Options:
    # 1. Run in the default asyncio loop's executor:
    result = await loop.run_in_executor(
        None, blocking_io)
    print('default thread pool', result)

    # 2. Run in a custom thread pool with concurrent.futures & Threads
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, blocking_io)
        print('custom thread pool (Blocking IO)', result)

    # 3. Run in a custom process pool with concurrent.futures & Process
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, cpu_bound)
        print('custom process pool (CPU Bound)', result)


asyncio.run(main())
