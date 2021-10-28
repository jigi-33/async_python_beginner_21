"""
The syntax 'async def' introduces either a native coroutine or an asynchronous generator.

The keyword 'await' passes function control back to the event loop. It suspends the execution of the
surrounding coroutine.

If Python encounters an 'await f()' expression in the scope of g() coroutine function,
this is how await tells the event loop: “Suspend execution of g() until I’m waiting on—the result
of f() is returned”.

Coroutines are repurposed generators that take advantage of the peculiarities of generator methods.

Old generator-based coroutines use "yield from" to wait for a coroutine result,
also as modern Python syntax in native coroutines simply replaces "yield from" with "await"
as the means of: SUSPEND and WAITING ON a coroutine's result.

The await is analogous to yield from, and it often helps to think of it;
using of "await" - is a signal that marks a break point.
It lets a coroutine temporarily suspend exec-n and permits the program-coro to come back here later.
"""
import asyncio


async def g():
    """ A coroutine may use await, return or yield keywords inside but all of these are optional """
    r = await f()  # suspend here and come back to g() execution when f() is free again(not busy)
    return r

"""
Using await and/or return creates a coroutine function.
To _call_ a coroutine function we must 'await' it to get its results.
We can _only_ use 'await' in the _body_ of coroutine function!

Simple examples of valid coroutine definitios:
"""


async def f(x):
    y = await z(x)  # VALID: 'await' + 'return' is allowed in coroutines.
    return y


async def g(x):
    yield x  # VALID: this is an async generator


async def m(x):
    yield from gen(x)  # NOT Valid: will raise SyntaxError


def m(x):
    y = await z(x)  # same: will raise SyntaxError (no 'async def' here so single await not allowed)
    return y


"""
These two coroutines are essentially equivalent (both are awaitable)
but the first is generator-based, while the second is a 'native' Python 3.5+ coroutine:
"""


@asyncio.coroutine
def py_below35_coro():
    """
    Generator-based coroutine - older syntax. This version of coro will be removed in Python 3.10.
    """
    yield from stuff()  # 'yield from' uzhe ne modno %-)


async def py35_and_higher_coro():
    """
    Native coroutine, actual syntax.
    """
    await stuff()
