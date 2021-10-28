import asyncio

"""
Python coroutines are awaitables and therefore can be awaited from other coroutines.
In the documentation the term 'coroutine' can be used for two closely related concepts:
a coroutine Function - an async def function
and
a coroutine Object: an object, returned by calling a coroutine func.

Asyncio also supports legacy generator-based coroutines.
"""


async def nested():
    return 42


async def main():
    # Nothing happens if we just call "nested()" ; a coroutine object created but not awaited,
    # won't run at all
    nested()  # However, a warning will be appear in the output string.

    # Let's do it differently now and await it
    print(await nested())  # will print "42"


asyncio.run(main())
