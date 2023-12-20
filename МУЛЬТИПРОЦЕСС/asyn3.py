# crypto api key secrets python
# https://docs.waves.exchange/ru/ccxt/#%D0%B7%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B0
# https://docs.ccxt.com/#/ccxt.pro.manual
# import ccxt
import time
# import datetime
import asyncio
import timeit

import asyncio, random
# https://imgvoid.medium.com/python-async-await-%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE-%D0%B1%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D1%8F-%D1%82%D0%B5%D0%BE%D1%80%D0%B8%D1%8F-%D0%B8-%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%B0-f970e29854b3
# Задача ограниченного буфера или Producer-consumer
# Состоит из ограниченного буфера и двух типов сопрограмм: производитель и потребитель. Поставщик добавляет элементы в очередь, а потребитель обрабатывает. Задача:
#
# Не дать производителю добавить больше элементов, чем может вместить очередь.
# Не дать потребителю запросить элемент из пустой очереди.
# Ответ: сценарий медленного потребителя для кооперативной многозадачности, семафоры для вытесняющей и параллелизма.
#
# Сценарий медленного потребителя — потребитель оповещает поставщика, когда взял и обработал данные, а поставщик ждет оповещение. Идеально подходят объекты Task и Queue:
async def consumer(buffer):
    while True:
        val = await buffer.get()
        await asyncio.sleep(1)
        buffer.task_done()
        print('Consumed', val)

async def producer(buffer):
    while True:
        val = random.randint(1, 100)
        await asyncio.sleep(1)
        await buffer.put(val)
        print('Produced', val)

async def main():
    buffer = asyncio.Queue(maxsize=3)
    producers = [asyncio.wait_for(
        asyncio.create_task(producer(buffer)), 10
    ) for _ in range(0, 4)]
    consumers = [asyncio.create_task(consumer(buffer)) for _ in range(0, 5)]
    await asyncio.gather(*producers)
    await buffer.join()
    for cons in consumers:
        cons.cancel()

try:
    asyncio.run(main())
except asyncio.TimeoutError:
    print('Done')

# async def fun1(key):
# 	print('yes',key)
# 	await asyncio.sleep(5)
#
#
# async def main():
# 	tasks=[]
# 	while True:
# 		timer = time.time()
# 		for key in range (10):
# 			tasks.append( asyncio.create_task(fun1(key)) )
#
# 		for task in tasks:
# 			await task
#
# 		await asyncio.sleep(10)
# 		print(time.time() - timer)
#
#
# asyncio.run(main())
# #
# # async def inf_loop():
# #     while True:
# #         print("Бесконечный цикл")
# #
# #
# # loop = asyncio.get_event_loop()
# #
# # asyncio.ensure_future(work())
# # loop.run_forever()