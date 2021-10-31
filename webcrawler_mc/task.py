import asyncio
from dataclasses import dataclass


@dataclass
class Task:
    """
    класс для "рядовых" задачек.
    """
    tid: int  # объявление атрибута класса с типом но без дефолтного значения

    async def perform(self, pool):
        print('start perform', self.tid)
        await asyncio.sleep(3)
        print('complete perform', self.tid)
        pass
