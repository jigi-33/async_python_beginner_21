import asyncio
import aiohttp

from dataclasses import field
from typing import Optional, ClassVar, Type

from marshmallow_dataclass import dataclass
from marshmallow import Schema, EXCLUDE

"""
Финальный код сервисной функции req() при использовании dataclasses и marshmallow.

Повторение еще раз - строку "Schema: ClassVar[Type[Schema]] = Schema" нужно добавлять,
чтобы было удобно вызывать процесс конвертации данных: GetResponse.Schema().load(data).

В результате мы сразу получим объект GetResponse.
Общий результат - описан формат ответа от API сервиса httpbin.org в виде дата-классов,
это позволит проще и быстрее дорабатывать основной код в дальнейшей разработке.
"""


@dataclass
class Headers:
    accept: str = field(metadata={'data_key': 'Accept'})
    accept_encoding: str = field(metadata={'data_key': 'Accept-Encoding'})
    host: str = field(metadata={'data_key': 'Host'})
    user_agent: str = field(metadata={'data_key': 'User-Agent'})
    x_amzn_trace_id: Optional[str] = field(default=None, metadata={'data_key': 'X-Amzn-Trace-Id'})

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetResponse:
    args: dict
    headers: Headers
    origin: str
    url: str

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


# data = {
#     "created_at": "2014-08-11T05:26:03.869245",
#     "email": "ken@yahoo.com",
#     "name": "Ken",
# }
# GetResponse.Schema().load(data)

async def req() -> GetResponse:
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            data = await resp.json()
            res = GetResponse.Schema().load(data)  # конвертация данных
            # print(res)  # отладочный
            return res


rez = asyncio.run(req())
print(rez)

# Должен вывести что-то в виде:
# GetResponse(args={}, headers=Headers(accept='*/*', accept_encoding='gzip, deflate', host='httpbin.org', user_agent='Python/3.9 aiohttp/3.7.4', x_amzn_trace_id='Root=1-617abf84-104fabc2421d1727362748d3'), origin='95.84.229.15', url='http://httpbin.org/get')
