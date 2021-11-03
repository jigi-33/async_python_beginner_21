import asyncio

"""
Shield example from kts.
"""

async def test():
    print(1)
    try:
        await asyncio.sleep(3)
        print('3 - cannot cancel with a shield')
    except BaseException:
        print("exception test")


async def main():
    t = asyncio.ensure_future(asyncio.shield(test()))  # or chng this to the next line, comment this
    # t = asyncio.create_task(test())

    print(2)
    await asyncio.sleep(1)
    t.cancel()
    await asyncio.sleep(5)
    print('finished!')


asyncio.get_event_loop().run_until_complete(main())
