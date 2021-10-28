import asyncio
import aiohttp  # web framework supports asyncio features
from codetiming import Timer  # see ex4_cooperative_concurency_nonblocking_calls.py

"""
In this example, the HTTP 'GET' calls are running asynchronously.
Other words, we’re effectively taking better advantage of the CPU by allowing it to make multiple
requests _at_once_
Because the CPU is so fast, this example could likely create as many tasks as there are URLs
In this (async) case, the program’s run time would be that of the single _slowest_ URL retrieval.
"""


async def task(name, work_queue):   # marks task() as an asynchronous function with async keyword
    timer = Timer(text=f"Task {name} elapsed time: {{:.1f}}")

    async with aiohttp.ClientSession() as session:  # an aiohttp session context manager with async!
        while not work_queue.empty():   # makes an HTTP GET call to the URL taken from work_queue
            url = await work_queue.get()
            print(f"Task {name} getting URL: {url}")
            timer.start()  # starts the timer instance
            async with session.get(url) as response:   # uses the session to get the text retrieved
                await response.text()                  # from the URL - asynchronously, of course.
            timer.stop()  # stops the timer instance & outputs the elapsed time since timer.start()


async def main():
    """
    This is the main entry point for the program code.
    """
    # Create the queue of work:
    work_queue = asyncio.Queue()

    # Put some work in the queue:
    for url in [
        "http://google.com",
        "http://yahoo.com",
        "http://linkedin.com",
        "http://apple.com",
        "http://microsoft.com",
        "http://habr.com",
        "http://rutube.ru",
    ]:
        await work_queue.put(url)

    # RUN ALL THE TASKS:

    # creates a Timer context manager that will output the elapsed time the entire 'while'-loop
    # batch to execute.
    with Timer(text="\nTotal elapsed time: {:.1f}"):
        await asyncio.gather(
            asyncio.create_task(task("One", work_queue)),
            asyncio.create_task(task("Two", work_queue)),
        )


if __name__ == "__main__":
    asyncio.run(main())  # start the prog.running asynchronously, also starts the internal eventloop
