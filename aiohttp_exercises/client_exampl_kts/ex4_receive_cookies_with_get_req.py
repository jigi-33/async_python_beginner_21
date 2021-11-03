"""
Пример4. Получаем cookies
"""
import asyncio
import aiohttp


async def req_cookies():
    async with aiohttp.ClientSession() as session:
        await session.get('http://httpbin.org/cookies/set?my_cookie=my_value')
        filtered = session.cookie_jar.filter_cookies('http://httpbin.org')

        print(filtered)


asyncio.run(req_cookies())
