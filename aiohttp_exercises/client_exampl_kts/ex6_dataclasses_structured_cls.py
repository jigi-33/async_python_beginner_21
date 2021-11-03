import asyncio
import aiohttp
from dataclasses import dataclass
from typing import Optional

# Здесь описываем структуру ответа метода API/get с помощью  датаклассов.
# Такая процедура называется мапингом (mapping).
# Для процесса мапинга и валидации есть универсальная библиотека https://marshmallow.readthedocs.io/en/stable
# А для нее есть дополнительная библиотека, которая связывает marshmallow и dataclasses.
# marshmallow_dataclass. Её интерпретация в следующем примере.


@dataclass
class Headers:
    accept: str
    accept_encoding: str
    host: str
    user_agent: str
    x_amzn_trace_id: Optional[str] = None


@dataclass
class GetResponse:
    args: dict
    headers: Headers
    origin: str
    url: str


async def req_proper() -> GetResponse:
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            data = await resp.json()
            headers_dict = data.get('headers', {})
            headers = Headers(
                accept=headers_dict['Accept'],
                accept_encoding=headers_dict['Accept-Encoding'],
                host=headers_dict['Host'],
                user_agent=headers_dict['User-Agent'],
                x_amzn_trace_id=headers_dict['X-Amzn-Trace-Id']
            )
            res = GetResponse(
                args=data['args'],
                headers=headers,
                origin=data['origin'],
                url=data['url']
            )
            return res


rez = asyncio.run(req_proper())

print(rez)
