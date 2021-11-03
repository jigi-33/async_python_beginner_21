"""
Делаем POST-запрос c JSON-телом
"""
import asyncio
import aiohttp


async def req_post_json():
    params = {'key1': 'value1', 'key2': 'value2'}

    async with aiohttp.ClientSession() as session:
        async with session.post('http://httpbin.org/post', json=params) as resp:
            print(await resp.text())


asyncio.run(req_post_json())
