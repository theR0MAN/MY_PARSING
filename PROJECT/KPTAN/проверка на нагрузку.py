import asyncio
import os
import sys
import time

import ccxt.pro as ccxt  # noqa: E402
import traceback
from PROJECT.my_lib import *


errorset=set()
aliveset=set()

# exshanges=['poloniexfutures']
# exshanges=['binance','bybit','mexc','gate','huobi','whitebit','poloniexfutures','okx']
# symbols=["BTC/USDT:USDT"]    #,"LTC/USDT:USDT"
godset = set()
exchanges = {}
exchdepth = {}
data = myload('Frez')
# {'bitopro', 'gate', 'okx', 'whitebit', 'hollaex', 'cryptocom', 'upbit', 'kraken', 'bitrue', 'probit', 'ascendex', 'gateio', 'bybit', 'kucoin', 'poloniex', 'huobi', 'bingx', 'kucoinfutures', 'binance', 'mexc', 'bitfinex2', 'bitmart', 'blockchaincom', 'bitmex', 'bitfinex', 'phemex', 'wazirx', 'binanceusdm', 'bitget', 'poloniexfutures'}
otborex= ( 'binance',)
# 'bybit','binance','poloniex',
# print(len(otborex))
# quit()
limit=150
for ex in otborex:
	exchanges[ex] = []
	exchdepth[ex] = 1
	count=0
	for sym in data[ex]['futures']:
		exchanges[ex].append(sym)
		count+=1
		if count> limit:
			break
	for sym in data[ex]['spot']:
		exchanges[ex].append(sym)
		count+=1
		if count> limit:
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

async def counter():
	global count
	count0=0
	tm0 = time.time()
	tmlast = time.time()
	while True:
		tm = time.time()
		await asyncio.sleep(0.05)
		tmlast = time.time()
		if tm0 + 1 <= tm:
			tm0 = tm
			print(' тормознули на ',round( tm-tmlast,2), ' answers ', count-count0," aliveeset ",len( aliveset) ," erreoeset ",len( errorset), errorset)

			count0=count

async def loader(ex):
	exchange = getattr(ccxt, ex)()
	try:
		await exchange.load_markets()
		print('load market ',ex)
	except Exception:
		print('ERROR load market ',ex)
		# traceback.print_exc()


async def poll(exch, symb, depth):
	global count
	exchange = getattr(ccxt, exch)()
	tm0 = time.time()
	while True:
		await asyncio.sleep(0.05)
		tm = time.time()
		if tm0 + 1 <= tm:
			tm0 = tm
			try:
				timer = time.time()
				stk=await exchange.watch_order_book(symb, depth)
				count+=1
				tm = time.time()
				aliveset.add(exch+symb)
				if exch+symb in errorset:
					print('ALIVE ',exch+symb)
					errorset.remove(exch+symb)
				# print(f" {exch}  {symb}   Ask= {stk['asks'][0][0]}  Bid= {stk['bids'][0][0]}  timestamp= {stk['timestamp']}")
				# if  stk['timestamp'] != None:
				# 	print(f" {exch}  {symb}   задержка получения {tm - timer}    отставание   {tm -stk['timestamp']/1000} ")
				# else:
				# 	print(f" {exch}  {symb}   задержка получения {tm-timer} ")
			except Exception:
				await  exchange.close()
				await asyncio.sleep(1)
				errorset.add(exch+symb)
				# print(exch, symb, "  ERROR")
				if exch+symb in aliveset:
					print('DEAD ',exch+symb)
					aliveset.remove(exch+symb)
				# print( "  ERRORset ",errorset)
				# traceback.print_exc()


async def main():
	taskslosd=[]
	for ex in exchanges:
		taskslosd.append(loader(ex) )

	task0=counter()
	tasks = []
	for ex in exchanges:
		for sym in exchanges[ex]:
			tasks.append(poll(ex, sym, exchdepth[ex]))

	await asyncio.gather(*taskslosd)
	await asyncio.gather(*tasks,task0)


asyncio.run(main())