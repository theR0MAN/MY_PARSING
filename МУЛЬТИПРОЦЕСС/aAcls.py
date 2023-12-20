import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    task1 = say_after(3, 'hello')
    task2 = say_after(3, 'world')
    print(f"started at {time.strftime('%X')}")
    await asyncio.gather(task1,task2)
    print(f"finished at {time.strftime('%X')}")
asyncio.run(main())

#
# async def main2():
#     tasks=[]
#     tasks.append(say_after(3, 'hello'))
#     tasks.append(say_after(2, 'world'))
#
#     eltasks = []
#     eltasks.append(say_after(3, 'elthello'))
#     eltasks.append(say_after(2, 'eltworld'))
#     print(f"started at {time.strftime('%X')}")
#     await asyncio.gather(*eltasks)
#     await asyncio.gather(*tasks)
#
#     print(f"finished at {time.strftime('%X')}")
#
# asyncio.run(main2())
#
#
# import asyncio
#
#
# async def factorial(name, number):
#     f = 1
#     for i in range(2, number + 1):
#         print(f"Task {name}: Compute factorial({i})...")
#         await asyncio.sleep(1)
#         f *= i
#     print(f"Task {name}: factorial({number}) = {f}")
#
#
# async def main():
#     args = [('A', 2), ('B', 3), ('C', 4)]
#     tasks = []
#     for arg in args:
#         # создаем задачи
#         task = factorial(*arg)
#         # складываем задачи в список
#         tasks.append(task)
#
#     # планируем одновременные вызовы
#     L = await asyncio.gather(*tasks)
#     # await tasks[0]
#     # print(L)
#
#
# if __name__ == '__main__':
#     # Запускаем цикл событий
#     results = asyncio.run(main())
