from dataclasses import field
from typing import Optional, ClassVar, Type

from marshmallow_dataclass import dataclass, class_schema
from marshmallow import Schema, EXCLUDE

"""
Schema exclusive syntax tip.
(два варианта описания датакласса с небольшим различием в синтаксисе)

строку Schema: ClassVar[Type[Schema]] = Schema нужно добавлять,
чтобы было удобно вызывать процесс конвертации данных: GetResponse.Schema().load(data).
В результате мы сразу получим объект GetResponse.
Но можно обойтись без этого синтаксиса и создать традиционную схему, как в первом примере
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

    class Meta:
        unknown = EXCLUDE


data = {
    "created_at": "2014-08-11T05:26:03.869245",
    "email": "ken@yahoo.com",
    "name": "Ken",
}

GetResponseSchema = class_schema(GetResponse)
GetResponseSchema().load(data)


# THE-BUSINESS-LOGIC-SIMILAR-TO-BELOW :
#  (vvvvvvv Optimized Edition vvvvvvvv)

@dataclass
class GetResponse:
    args: dict
    headers: Headers
    origin: str
    url: str

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


GetResponse.Schema().load(data)
