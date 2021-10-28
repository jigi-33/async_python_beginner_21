# The 'rand.py' sample code from RealPython advanced tutorial.

import asyncio
import random

# ANSI colors:
c = (
    "\033[0m",   # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)


async def makerandom(idx: int, threshold: int = 6) -> int:
    """ 'Central' & single coroutine """

    print(c[idx + 1] + f"Initiated makerandom({idx}).")
    i = random.randint(0, 10)

    while i <= threshold:
        print(c[idx + 1] + f"makerandom({idx}) == {i} too low; retrying.")
        await asyncio.sleep(idx + 1)
        i = random.randint(0, 10)
    print(c[idx + 1] + f"---> Finished: makerandom({idx}) == {i}" + c[0])
    return i


async def main():
    """
    Most programs will contain small, modular coroutines.
    and one wrapper function that serves to chain each of the smaller coroutines together, main()
    It's then used to gather tasks(futures) by mapping the central coroutine across the pool.
    In this case, the pool is range(3) tuple.
    """
    res = await asyncio.gather(
        *(makerandom(i, 10 - i - 1) for i in range(3))  # CPU-bound operation inside of the pool :)
    )
    return res


if __name__ == "__main__":
    random.seed(444)
    r1, r2, r3 = asyncio.run(main(), debug=True,
                             )
    print()
    print(f"r1: {r1}, r2: {r2}, r3: {r3}")
