import asyncio

counter = 0
res = "Успех"
locker = asyncio.Lock()

# Задача решена:
# TODO используя Lock не допустить длительного сна
# убирать sleep() или изменять время сна нельзя


async def worker():
    global locker, counter

    async with locker:
        await asyncio.sleep(0.1)
        counter += 1
        print(counter)
        if counter > 1:
            await asyncio.sleep(5)
        else:
            await asyncio.sleep(0.1)
        counter -= 1
    print('the worker released lock')


async def main():
    global locker, res
    # Create and acquire a shared lock                      \ это все ИЗЛИШНЕ:
    # print('acquiring the lock before starting coros...')  | все это включено
    # await locker.acquire()                                / в к/м with locker

    try:
        await asyncio.wait_for(
            asyncio.wait([worker(), worker(), worker(), worker()]),
            timeout=1
        )
    except asyncio.TimeoutError:
        res = "Долгое время выполнения!"
    finally:
        print('All the workers are perform his work...')


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.close()  # с v 3.9 способен ругаться, т.е. можно опускать.

    print(res)
