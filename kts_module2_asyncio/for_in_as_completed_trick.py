import asyncio
from random import randrange

"""
asyncio.as_completed() 'external' example.

This demonstrates how as_complete will yield the first task to complete,
followed by the next quickest, and the next until all tasks are completed.

as_completed возвращает итератор результатов задач в порядке их _исполнения_, в отличие от gather()

Очень удобный в практике метод!
"""

async def foo(n):
    s = randrange(10)
    print(f"{n} task will sleep for: {s} random secs")
    await asyncio.sleep(s)
    return f"{n}!"


async def main():
    counter = 0
    coros = [
        foo("A"), foo("B"), foo("C"),
    ]
    for future in asyncio.as_completed(coros):
        n = "fastest" if counter == 0 else "next quickest"
        counter += 1
        result = await future

        print(f"The {n} result was: {result}")


asyncio.run(main())
