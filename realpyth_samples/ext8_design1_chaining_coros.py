# originally chained.py in 'extended' article on RealPython
# URGENT: it has time's perf_counter function in action!

import asyncio
import random
import time

"""
the Chaining Coroutines design pattern (Deal example!)

A key feature of coroutines is that they can be chained together
We remember, a coroutine object is awaitable, so another coroutine can await it,
this allows you to break programs into smaller, manageable, recyclable coroutines.

Here, each task - Future - is composed of a set of coroutines that explicitly await each other
and pass through a single input per chain.
"""


async def part1(n: int) -> str:
    i = random.randint(0, 10)
    print(f"part1({n}) sleeping for {i} seconds.")
    await asyncio.sleep(i)
    result = f"result{n}-1"
    print(f"Returning chain's part1({n}) == {result}.")
    return result


async def part2(n: int, arg: str) -> str:
    i = random.randint(0, 10)
    print(f"part2{n, arg} sleeping for {i} seconds.")
    await asyncio.sleep(i)
    result = f"result{n}-2 derived from {arg}"
    print(f"Returning part2{n, arg} == {result}.")
    return result


async def chain(n: int) -> None:
    start = time.perf_counter()
    p1 = await part1(n)
    p2 = await part2(n, p1)
    end = time.perf_counter() - start
    print(f"-->Chained result{n} => {p2} (took {end:0.2f} seconds).")


async def main(*args):
    await asyncio.gather(*(chain(n) for n in args))


if __name__ == "__main__":
    """
    NOTE: In this setup, the runtime of main() will be equal to the maximum runtime of the tasks
    that it gathers together and schedules
    """
    import sys
    random.seed(444)  # типа "встряхнуть" рандом-генератор
    args = [1, 2, 3] if len(sys.argv) == 1 else map(int, sys.argv[1:])

    start = time.perf_counter()
    asyncio.run(main(*args))
    end = time.perf_counter() - start

    print(f"Program finished in {end:0.2f} seconds.")
