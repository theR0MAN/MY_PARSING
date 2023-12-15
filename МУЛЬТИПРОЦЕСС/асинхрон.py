import asyncio
import time



a=[]

async  def my():
    while True:
        print(a)
        await asyncio.sleep(11)

async def fun0():
    while True:
        a.append('shit')
        await asyncio.sleep(5)
        # return a

async def fun2(x):
    n=0
    tm0=int (time.time())
    while True:
        tm=int(time.time())
        if tm0!= tm:
            tm0=tm
            n+=1
            # print(x,'  func',n*x)
            a.append(n*x)
        await asyncio.sleep(0.005)
        # return n


async def main(num):
    tasks=[]
    taskmaim=asyncio.create_task(my())
    task0= asyncio.create_task(fun0())
    for i in range (num):
        tasks.append(asyncio.create_task(fun2(i)))

    await  task0
    for task in tasks:
        await task
    await  taskmaim


asyncio.run(main(10))



