import asyncio
import os
import sys
import time

import ccxt.pro as ccxt  # noqa: E402
import traceback
from PROJECT.my_lib import *


errorset=set()
aliveset=set()


godset = set()
exchanges = {}
exchdepth = {}
data = myload('Frez')
# {'bitopro', 'gate', 'okx', 'whitebit', 'hollaex', 'cryptocom', 'upbit', 'kraken', 'bitrue', 'probit', 'ascendex', 'gateio', 'bybit', 'kucoin', 'poloniex', 'huobi', 'bingx', 'kucoinfutures', 'binance', 'mexc', 'bitfinex2', 'bitmart', 'blockchaincom', 'bitmex', 'bitfinex', 'phemex', 'wazirx', 'binanceusdm', 'bitget', 'poloniexfutures'}
otborex= ( 'poloniexfutures',)
# 'bybit','binance','poloniex',

for ex in otborex:
	exchanges[ex] = []
	exchdepth[ex] = 1
	countf=0
	counts = 0
	count=counts+countf
	for sym in data[ex]:
		# if'-231222' not in sym:
		exchanges[ex].append(sym)
		


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

async def poll(exch, symb, depth,ct,always):
	global count
	exchange = getattr(ccxt, exch)()
	tm0 = time.time()
	while True:

		await asyncio.sleep(0.05)
		tm = time.time()
		if tm0 + 1 <= tm:
			tm0 = tm
			try:
				print(" aliveeset ",len( aliveset) ," erreoeset ",len( errorset), errorset)
				timer = time.time()
				stk=await exchange.watch_order_book(symb, depth)
				count+=1
				tm = time.time()
				aliveset.add(exch+symb)
				if exch+symb in errorset:
					print('ALIVE ',exch+symb)
					errorset.remove(exch+symb)
			except Exception:
				await  exchange.close()
				await asyncio.sleep(1)
				errorset.add(exch+symb)
				if exch+symb in aliveset:
					print('DEAD ',exch+symb)
					aliveset.remove(exch+symb)
					
			if len(errorset) == 0 and len(aliveset) != 0 and len(aliveset) >= ct:
				# print('break')

				if not always:
					# await  exchange.close()
					break



async def main():

	lim=5
	for ex in exchanges:
		LN = len(exchanges[ex])
		print(f" {ex} get symbols {LN}  ")
		while lim <= LN:
			tasks = []
			cot=0
			for sym in exchanges[ex][:lim]:
				cot+=1
				tasks.append(poll(ex, sym, exchdepth[ex],cot,False))
			print('zapusk ',lim)
			await  asyncio.gather(*tasks)
			print('ZAYABIS')
			# print(f' lim {lim}  LN   {LN}')
			# if lim == LN:
			# 	break
			lim=lim+5
			# if lim>LN:
			# 	lim=LN

		task0 = counter()
		tasks = []
		for sym in exchanges[ex]:
			tasks.append(poll(ex, sym, exchdepth[ex], -1, True))
		print('zapusk FINAL')
		await  asyncio.gather(*tasks,task0)


asyncio.run(main())