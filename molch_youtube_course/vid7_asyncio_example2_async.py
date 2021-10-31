import asyncio
import aiohttp
from time import time


"""
Асинхронный вариант качалки.

Note: в идеале желательно не смешивать синхронный код и асинхронный.
"""

def write_image(data):   # можно прикрутить даже aiofiles, которая пишет в разных _потоках_
    filename = f'file-{int(time() * 1000)}.jpeg'
    with open(filename, 'wb') as file:
        file.write(data)


async def fetch_content(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()  # возвращает бинарные данные
        write_image(data)  # внутри асинхронных функций можно использовать синхр. код и вызыв синхр. ф-и


async def main():
    url = 'https://loremflickr.com/320/240'
    tasks = []

    async with aiohttp.ClientSession() as session:
        for i in range(10):
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)

        await asyncio.gather(*tasks)  # список tasks будет распакован на все элементы


if __name__ == '__main__':
    t0 = time()
    asyncio.run(
        main()
    )
    print(time() - t0)
