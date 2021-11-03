import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            print(resp.status)
            print()
            print(await resp.text())


def run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        main()
    )


if __name__ == '__main__':
    run()
