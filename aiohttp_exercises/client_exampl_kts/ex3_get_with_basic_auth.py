"""
Пример3. Делаем GET-запрос c Basic Auth авторизацией
"""

import asyncio
import aiohttp


async def req_basic_auth():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get', auth=aiohttp.BasicAuth('user', 'pass')) as resp:
            print(await resp.text())


asyncio.run(req_basic_auth())
