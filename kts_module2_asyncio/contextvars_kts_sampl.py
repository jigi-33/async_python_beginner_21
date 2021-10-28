import asyncio
from contextvars import ContextVar


global_var: ContextVar[int] = ContextVar('global_var', default=4,)


async def printer(i: int):
    print(f"printer {i} global_var={global_var.get()}")
    global_var.set(i)
    print(f"printer {i} global_var={global_var.get()}")


async def main():
    await asyncio.gather(*[printer(i + 1) for i in range(3)])


asyncio.run(main())
