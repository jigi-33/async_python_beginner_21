"""
Пример2. Делаем POST-запрос c заголовками
"""
import asyncio
import aiohttp


async def req_headers():
    headers = {'key1': 'value1', 'key2': 'value2'}
    cookies = {'key1': 'value1'}

    async with aiohttp.ClientSession() as session:
        async with session.post('http://httpbin.org/post', headers=headers, cookies=cookies) as resp:
            print(await resp.text())


asyncio.run(req_headers())
