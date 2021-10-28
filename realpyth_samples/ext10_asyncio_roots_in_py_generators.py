# "AsyncIO’s roots in generators" (based on RealPython advanced article)

import asyncio


@asyncio.coroutine
def gen_based_coro():
    """ Generator based coroutine"""
    # No need to build these yourself, but be aware of what they are
    s = yield from stuff()  # yield from - the old syntax (may be obsolete from Py3.10)
    return s


async def py35_and_above_modern_coro():
    """ Native coroutine, modern syntax """
    s = await stuff()
    return s


async def stuff():
    return 0x10, 0x20, 0x30
