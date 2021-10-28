import asyncio

"""
Neither asynchronous generators nor comprehensions make the iteration _concurrent_ !

The asynchronous iterators and asynchronous generators are not designed to concurrently map
some function over a sequence or iterator.

They’re merely designed to let the enclosing coroutine allow other tasks to take their turn.
The "async for" and "async with" statements are designed to the extent that using plain for or with
would "break" the nature of await in the coroutine...
"""


async def mygen(u: int = 10):
    """
    Yield powers of 2
    """
    i = 0
    while i < u:
        yield 2 ** i
        i += 1
        await asyncio.sleep(0.1)


async def main():
    # this does NOT introduce concurrent execution. It is meant to show syntax only...
    g = [i async for i in mygen()
         ]
    f = [j async for j in mygen() if not (j // 3 % 5)
         ]

    return g, f


g, f = asyncio.run(main())

print(g, '\n')
print(f)
