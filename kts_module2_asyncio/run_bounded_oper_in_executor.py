import asyncio
import concurrent.futures as executor


def blocking_io():
    # File syncrous operations (such as logging) can block the
    # event loop: run them in a Thread-pool.
    with open('/dev/urandom', 'rb') as f:
        return f.read(100)


def cpu_bound():
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a Process-pool.
    return sum(i * i for i in range(10 ** 7))


async def main():
    loop = asyncio.get_running_loop()  # return running EvtLoop in curr. thread

    # Options:
    # 1. Run in the default loop's executor - it's a threaded by default
    # (Here's no "with" context manager).
    result = await loop.run_in_executor(
        None, blocking_io)
    print('Default (None) thread pool:', result, '\n')

    # 2. Run in a custom thread pool:
    with executor.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, blocking_io)
        print('custom Thread Pool:', result, '\n')

    # 3. Run in a custom process pool:
    with executor.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, cpu_bound)
        print('custom Process Pool: the summ is', result, '\n')


asyncio.run(main())
