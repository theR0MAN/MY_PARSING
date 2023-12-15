# crypto api key secrets python
# https://docs.waves.exchange/ru/ccxt/#%D0%B7%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B0
# https://docs.ccxt.com/#/ccxt.pro.manual
# import ccxt
import time
# import datetime
import asyncio
import timeit


async def fun1(key):
	print('yes',key)
	await asyncio.sleep(5)


async def main():
	tasks=[]
	while True:
		timer = time.time()
		for key in range (10):
			tasks.append( asyncio.create_task(fun1(key)) )

		for task in tasks:
			await task

		await asyncio.sleep(10)
		print(time.time() - timer)


asyncio.run(main())
#
# async def inf_loop():
#     while True:
#         print("Бесконечный цикл")
#
#
# loop = asyncio.get_event_loop()
#
# asyncio.ensure_future(work())
# loop.run_forever()