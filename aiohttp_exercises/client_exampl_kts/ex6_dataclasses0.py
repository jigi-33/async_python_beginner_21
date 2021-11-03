import asyncio
import aiohttp
"""
Заготовка для урока о датаклассах
"""


async def req():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            return await resp.json()


res = asyncio.run(req())

print(res)
