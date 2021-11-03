"""
Пример1. Делаем GET-запрос c параметрами, получаем данные, статусы, заголовки
"""
import aiohttp
import asyncio


async def req1():
    params = {'key1': 'value1', 'key2': 'value2'}

    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get', params=params) as resp:

            print(await resp.read(), '\n')
            await asyncio.sleep(1)

            print(await resp.text(), '\n')
            await asyncio.sleep(1)

            print(await resp.json(), '\n')
            await asyncio.sleep(1)

            print(resp.status)
            print(resp.headers)


asyncio.run(req1())
