import asyncio
import os
import sys
import time

from multiprocessing import Process

import ccxt.pro as ccxt  # noqa: E402
import traceback
from PROJECT.my_lib import *

# exshanges=['poloniexfutures']
# exshanges=['binance','bybit','mexc','gate','huobi','whitebit','poloniexfutures','okx']
# symbols=["BTC/USDT:USDT"]    #,"LTC/USDT:USDT"

data = myload('Frez')
# {'bitopro', 'gate', 'okx', 'whitebit', 'hollaex', 'cryptocom', 'upbit', 'kraken', 'bitrue', 'probit', 'ascendex', 'gateio', 'bybit', 'kucoin', 'poloniex', 'huobi', 'bingx', 'kucoinfutures', 'binance', 'mexc', 'bitfinex2', 'bitmart', 'blockchaincom', 'bitmex', 'bitfinex', 'phemex', 'wazirx', 'binanceusdm', 'bitget', 'poloniexfutures'}
otborex = ('binance', 'bybit', 'poloniex','okx','whitebit','upbit','kraken',)
# 'bybit','binance','poloniex',
# print(len(otborex))
# quit()
limit = 50


def mfun(ex):
	errorset = set()
	aliveset = set()
	godset = set()
	exchanges = {}
	exchdepth = {}

	exchanges[ex] = []
	exchdepth[ex] = 1
	count1 = 0
	for sym in data[ex]['futures']:
		exchanges[ex].append(sym)
		count1 += 1
		if count1 > limit:
			break
	for sym in data[ex]['spot']:
		exchanges[ex].append(sym)
		count1 += 1
		if count1 > limit:
			break

	print(f" {ex} get symbols {len(exchanges[ex])}  ")
	time.sleep(2)

	exchdepth['kucoinfutures'] = 20
	exchdepth['kraken'] = 10
	exchdepth['kucoin'] = 20
	exchdepth['bitfinex2'] = 25
	exchdepth['bitmex'] = None
	exchdepth['bitopro'] = None  # 5
	exchdepth['bitfinex'] = 25
	exchdepth['bingx'] = 20
	exchdepth['poloniexfutures'] = 5
	exchdepth['huobi'] = 20
	exchdepth['binanceusdm'] = 5
	exchdepth['binance'] = 5
	exchdepth['coinex'] = None
	exchdepth['bitrue'] = None

	# huobi  - только фьючи оставить, иначе ошибка

	async def counter(ex):

		tm0 = time.time()
		tmlast = time.time()
		while True:
			tm = time.time()
			await asyncio.sleep(0.05)
			tmlast = time.time()
			if tm0 + 1 <= tm:
				tm0 = tm
				print(ex, ' тормознули на ', round(tm - tmlast, 2),  " aliveeset ", len(aliveset), " erreoeset ", len(errorset), errorset)


	async def poll(exch, symb, depth):
		exchange = getattr(ccxt, exch)()
		tm0 = time.time()
		while True:
			await asyncio.sleep(0.1)
			tm = time.time()
			if tm0 + 1 <= tm:
				tm0 = tm
				try:
					timer = time.time()
					stk = await exchange.watch_order_book(symb, depth)
					tm = time.time()
					aliveset.add(exch + symb)
					if exch + symb in errorset:
						print('ALIVE ', exch + symb)
						errorset.remove(exch + symb)
				# print(f" {exch}  {symb}   Ask= {stk['asks'][0][0]}  Bid= {stk['bids'][0][0]}  timestamp= {stk['timestamp']}")
				# if  stk['timestamp'] != None:
				# 	print(f" {exch}  {symb}   задержка получения {tm - timer}    отставание   {tm -stk['timestamp']/1000} ")
				# else:
				# 	print(f" {exch}  {symb}   задержка получения {tm-timer} ")
				except Exception:
					await  exchange.close()
					await asyncio.sleep(0.5)
					errorset.add(exch + symb)
					# print(exch, symb, "  ERROR")
					if exch + symb in aliveset:
						print('DEAD ', exch + symb)
						aliveset.remove(exch + symb)
					# print( "  ERRORset ",errorset)
					# traceback.print_exc()

	async def main(ex):

		task0 = counter(ex)
		tasks = []

		for sym in exchanges[ex]:
			tasks.append(poll(ex, sym, exchdepth[ex]))

		await asyncio.gather(*tasks, task0)

	asyncio.run(main(ex))

if __name__ == "__main__":
	for ex in otborex:
		Process(name='worker ' + ex, target=mfun, args=(ex,)).start()


