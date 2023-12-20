import asyncio
import time


import platform

print(platform.python_version())

a=[]


async def fun0(num):
    while True:
        await asyncio.sleep(5)
        print( num)


async def main(num):

    # for i in range (10):
    #     task=asyncio.create_task(fun0(i))
    task1 = asyncio.create_task(fun0(1))
    task2 = asyncio.create_task(fun0(2))
    task3 = asyncio.create_task(fun0(3))
    # await task1
    # await task2
    # await task3

asyncio.run(main(10))



