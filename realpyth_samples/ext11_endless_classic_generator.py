from itertools import cycle

"""
The "loop"-generator example.

A generator, pauses each time it hits a "yield" and goes no further. And, as 2nd, we can send
a value into a generator as well through its .send() method. This allows generators (and coroutines)
to call ("await") each other without blocking!

The "await" keyword behaves similarly yield,
marking a break point at which the coroutine suspends itself and lets other coroutines work.
"Suspended" in this case, means a coroutine that has temporarily ceded (уступает) control
but not totally exited or finished.

Keeps in mind that yield (and by extension - "yield from") and await k/words
mark a breakpoint in a generator’s execution as in this example.
"""


def endless_gen():
    """Yields 9, 8, 7, 6, 9, 8, 7, 6, ... and forever"""
    yield from cycle(
        (9, 8, 7, 6),
    )


e = endless_gen()
total = 0
for i in e:
    if total < 30:
        print(i, end=" ")
        total += i
    else:
        print()
        # Pause execution; we can resume later...
        break


# Resume
print(next(e), next(e), next(e))
print(next(e), next(e))
