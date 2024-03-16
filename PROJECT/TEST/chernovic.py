
import time

import asyncio

async def print_numbers():
    for i in range(10):
        await asyncio.sleep(1)
        print(i)


async def main():
    task2 = asyncio.create_task(print_numbers())
    await task2


asyncio.run(main())