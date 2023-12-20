
import ccxt.pro as ccxt
from PROJECT.my_lib import *
import time
import datetime
import asyncio
import traceback

ask0 = {}
bid0 = {}
count = 0

data=myload('Frez')

async def loader(birza,ex):
	try:
		await asyncio.wait_for(birza.load_markets(),300)
		print('load market ', birza,'   ',ex)
	except Exception:
		print('ERROR load market ', birza,'   ',ex)
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
				orderbook = await asyncio.wait_for(M.watch_order_book(sym,None), 1000)
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
					timer = time.time() - start
					print(ex, '  ', timer)
			except asyncio.TimeoutError:
				print(ex,' imeoutError', sym)
			except Exception:
				print(ex,' ERROR', sym)
				traceback.print_exc()


# https://superfastpython.com/asyncio-coroutine-was-never-awaited/


async def main():
	countex=0
	countsyms=0
	tasksload = []
	tasks = []
	birzas=dict()
	for ex in data:
		if ex in ['bybit'] :  #ex in ['binance','bybit','gate','kraken']
			birzas[ex] = getattr(ccxt, ex)()
			tasksload.append(loader(birzas[ex],ex))
			ask0[ex] = {}
			bid0[ex] = {}
			for sym in data[ex]:
				if True:    #sym in ["BTC/USDT",'ETH/USDT']  ':USDT'not in sym
					tasks.append(fun1(birzas[ex], ex, sym))
					countex+=1
					if countex >350 :
						break
					print(sym)
					ask0[ex][sym]=0
					bid0[ex][sym] = 0
	# markets = await self.fetch_markets(params)
	print('start load tasks')
	await asyncio.gather(*tasksload)
	print('STOP load tasks')
	print('start MAIN tasks')
	await asyncio.gather(*tasks)
	print('STOP MAIN tasks')



asyncio.run(main())