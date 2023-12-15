
import ccxt.pro as ccxt
from PROJECT.my_lib import *
import ccxt as ccxt0
import time
import datetime
import asyncio
import traceback

ask0 = {}
bid0 = {}
count = 0

data=myload('Frez')

async def loader(birza):
	try:
		await asyncio.wait_for(birza.load_markets(),20)
		# await birza.close()
		print('load market ', birza)
	except Exception:
		print('ERROR load market ', birza)
		traceback.print_exc()






async def fun1(M,ex,sym):
	global count
	tm0 = int(time.time())
	while True:
		await asyncio.sleep(0.05)
		tm = time.time()
		if tm0 +1<= tm:
			tm0 = tm
			try:
				start=time.time()
				orderbook = await asyncio.wait_for(M.watch_order_book(sym), 100)
				count += 1
				# print(ex)
				# print(orderbook)
				# print(time.time())
				bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else 0
				ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else 0
				# timer = time.time() - start
				# print(ex, '  ', timer)
				# print(sym, "   ", ask, "   ", bid)
				if (ask0[ex][sym] != ask or bid0[ex][sym] != bid):
					ask0[ex][sym] = ask
					bid0[ex][sym] = bid
					print(ex,' ',sym, "   ", ask, "   ", bid)
			except asyncio.TimeoutError:
				print(ex,' imeoutError', sym)
			except Exception:
				print(ex,' ERROR', sym)
				traceback.print_exc()


# async def LM():
# 	await ccxt.gate().load_markets()
# 	await ccxt.binance().load_markets()
# 	# await ccxt.gate().close()
# 	# await ccxt.binance().close()
# https://superfastpython.com/asyncio-coroutine-was-never-awaited/


async def main():
	tasksload = []
	tasks = []
	birzas=dict()
	for ex in data:
		if  ex in ['binance','bybit','gate']:
			birzas[ex] = getattr(ccxt, ex)()
			tasksload.append(asyncio.create_task(loader(birzas[ex])))
			ask0[ex] = {}
			bid0[ex] = {}
			for sym in data[ex]:
				if sym in ["BTC/USDT",'ETH/USDT']:
					tasks.append(asyncio.create_task(fun1(birzas[ex], ex, sym)))
					ask0[ex][sym]=0
					bid0[ex][sym] = 0
	# markets = await self.fetch_markets(params)
	await asyncio.gather(*tasksload)
	await asyncio.gather(*tasks)

# asyncio.run(Loadmain())
asyncio.run(main())
