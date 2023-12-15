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

async def counter():
	global count
	while True:
		await  asyncio.sleep(1)
		print(count)
		count = 0


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
				orderbook = await asyncio.wait_for(M.watch_order_book(sym), 30)
				count += 1
				print(ex)
				print(orderbook)
				print(time.time())
				bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else 0
				ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else 0
				# timer = time.time() - start
				# print(ex, '  ', timer)
				# print(sym, "   ", ask, "   ", bid)
				if (ask0[ex][sym] != ask or bid0[ex][sym] != bid):
					ask0[ex][sym] = ask
					bid0[ex][sym] = bid
					# print(ex,' ',sym, "   ", ask, "   ", bid)
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

async def main():
	tasks = []
	birzas=dict()
	for ex in data:
		birzas[ex] = getattr(ccxt, ex)()

	# for ex in data:
	# 	for sym in data[ex]:
	# 		print(type(birzas[ex]))
	# 		tasks.append(asyncio.create_task(fun1(birzas[ex],ex, sym)))

	ask0['kraken']={}
	bid0['kraken']={}
	ask0['kraken']['BTC/USDT'] = 0
	bid0['kraken']['BTC/USDT'] = 0

	ask0['gate'] = {}
	bid0['gate'] = {}
	ask0['gate']['BTC/USDT'] = 0
	bid0['gate']['BTC/USDT'] = 0

	ask0['binance'] = {}
	bid0['binance'] = {}
	ask0['binance']['BTC/USDT'] = 0
	bid0['binance']['BTC/USDT'] = 0

	ask0['bybit']={}
	bid0['bybit']={}
	ask0['bybit']['BTC/USDT'] = 0
	bid0['bybit']['BTC/USDT'] = 0

	# ccxt0.kraken().load_markets()
	# ccxt0.gate().load_markets()
	# ccxt0.binance().load_markets()
	# ccxt0.bybit().load_markets()
	# await ccxt.gate().close()
	# await ccxt.binance().close()

	task= asyncio.create_task(fun1(ccxt.kraken(),'kraken', 'BTC/USDT'))
	task2 = asyncio.create_task(fun1(ccxt.gate(), 'gate', 'BTC/USDT'))
	task3 = asyncio.create_task(fun1(ccxt.binance(), 'binance', 'BTC/USDT'))
	task4 = asyncio.create_task(fun1(ccxt.bybit(), 'bybit', 'BTC/USDT'))
	await task
	await task2
	await task3
	await task4
	# task0 = asyncio.create_task(counter())
	# await task0
	# await asyncio.gather(*tasks)


asyncio.run(main())
