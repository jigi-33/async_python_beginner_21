"""
This code makes use of Python async features using asyncio/await provided in Python 3 (from ver 3.7)

The time and queue modules have been replaced with the asyncio package.
This gives your program access to asynchronous friendly (non-blocking) sleep and queue functionality
In the task() defines it as asynchronous with the addition of the 'async' prefix on line 29.
This indicates to Python that the function will be asynchronous.

An asynchronous program runs in a _single_thread_ of execution.
But each task was able to run with "await asyncio.sleep(delay)" syntax at the same time!
The context switch from one section of code to another that would affect data is completely
in our control.
This means we can atomize and complete all shared memory data access before making a context switch.
This simplifies the shared memory problem inherent in threaded code.
"""

import asyncio
from codetiming import Timer
"""
All of the sample code using a module called codetiming to time and output how long sections of code
took to execute. There is a great article here: https://realpython.com/python-timer/ that goes into
depth about the codetiming module and how to use it smartly. If you are writing code that needs to
include timing functionality, Geir Arne’s codetiming module is well worth looking at.
to install it type: pip install codetiming
"""


async def task(name, work_queue):  # the async keyword in front of the task() definition.
                                   # this informs the program in that task can run _asynchronously_
    timer = Timer(text=f"Task {name} elapsed time: {{:.1f}}")  # creates the Timer instance used to
                                        # measure the time taken for each iteration of the task loop
    while not work_queue.empty():
        delay = await work_queue.get()
        print(f"Task {name} running")
        timer.start()   # starts the timer instance
        await asyncio.sleep(delay)  # non-blocking asyncio.sleep(delay), which also yields control
                                    # (or switches contexts) back to the main event loop of asyncio.
                                    # Use with await keyword.
        timer.stop()  # stops the timer and outputs the elapsed time since timer.start() was called.


async def main():
    """
    the main entry point for the program
    """
    # Create the Queue-of-work instance:
    work_queue = asyncio.Queue()  # creates the non-blocking asynchronous work_queue.

    # Put some work in the Queue:
    for work in [15, 10, 5, 2]:     # put work into work_queue in an asynchronous pipe
        await work_queue.put(work)  # using the await keyword, too

    # RUN ALL THE TASKS:
    with Timer(text="\nTotal elapsed time: {:.1f}"):  # creates a Timer context manager that will
                                     # output the elapsed time the entire 'while' loop took 2execute

        # There’s a call to await asyncio.gather(...). This tells asyncio about two things:
        # - Create two tasks based on task() and start running them.
        # - Wait for both of these to be completed before moving forward.
        await asyncio.gather(
            asyncio.create_task(task("One", work_queue)),
            asyncio.create_task(task("Two", work_queue)),
        )


if __name__ == "__main__":
    asyncio.run(main())  # start the prog. running asynchronously;also starts the internal eventloop
