import asyncio
import datetime
import os
import sys
import time

from multiprocessing import Process

import ccxt.pro as ccxt1  # noqa: E402
import traceback
from PROJECT.my_lib import *
from PROJECT.KPTAN.SBOR.getmaindata import rez_dict

#
# 'binance' 5,8/137 - 137  42- соберем фьючи, слишком тяжелый   на Каймановых островах
# 'bybit' 4,4/224 -224    20 круто    Дубай  -надо собрать всё ,но соберем фьючи
# 'bingx' 2,1 / 230  -240  9- собрать всё   -сингапур
# 'bitfinex' 0,4 /65 -65   6- всё    на Британских Виргинских острова
# 'bitfinex2'  0,6/104 -104    6-всё
# 'poloniex' 1,2 /94 - 50  12- всё  США
# 'kucoinfutures' 0,7/120 -120  6 все
# 'binanceusdm'- 0,7/122 -122   6-шикарно   сша
# 'whitebit' 0,7/135 -90   5- литва - ну нах но соберем
# 'phemex'  2,3/180 -110    12- сингапур - очень зашибок до 180 символов только фьючи возьмем
# huobi  - только фьючи оставить, иначе ошибка


# 'bitfinex2'

all= ('bitfinex2','poloniex','bingx', 'whitebit',) #,'whitebit',
# all= ('bingx','bitfinex','bitfinex2','poloniex','kucoinfutures','binanceusdm','whitebit')
# onlyfut=('bybit','binance','phemex',"huobi")
onlyfut=() #'bybit','binance','huobi','binanceusdm',


all = ('bitfinex2',)



count=0
def mfun(ex,symbols,depth):
	ccxt=ccxt1
	errorset=set()
	aliveset=set()
	print(f" {ex} get symbols {len(symbols)} ")
	time.sleep(2)

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
				print(ex,' тормознули на ',round( tm-tmlast,2), ' answers ', count-count0," aliveeset ",len( aliveset) ," erreoeset ",len( errorset), errorset)
				count0=count


	async def poll(exch, symb, depth,stsl,num):
		global count
		exchange = getattr(ccxt, exch)()
		tm0 = time.time()
		await asyncio.sleep(1)#stsl
		print("START ",exch,symb,"  ",num)

		while True:
			await asyncio.sleep(0.05)
			tm = time.time()
			dat = datetime.datetime.utcfromtimestamp(tm)
			if dat.second<=3:
				print(' BREAK TO TIME')
				break
			if tm0 + 1 <= tm:
				tm0 = tm
				try:
					timer = time.time()
					stk=await asyncio.wait_for(exchange.watch_order_book(symb, depth),100)
					count+=1
					tm = time.time()
					print(f" {exch}  {symb}   задержка получения {tm - timer} ")
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

	async def main(ex):
		# data = rez_dict(30, 40, 50, all)
		task0=counter()
		tasks = []
		stsl = 0
		num = 0
		for sym in symbols:
			num+=1
			stsl+=2
			tasks.append(poll(ex, sym, depth,stsl,num))
		await asyncio.gather(*tasks,task0)

		while True:
			# data = rez_dict(30, 40, 50, all)
			tasks = []
			stsl = 0
			num = 0
			for sym in symbols:
				num += 1
				stsl += 2
				tasks.append(poll(ex, sym, depth, stsl, num))
			print("FIGACHIM")
			break
			# await asyncio.gather(*tasks, task0)


	asyncio.run(main(ex))


if __name__ == "__main__":
	data = rez_dict( 30, 40, 50, all)
	exchanges = {}
	for ex in all:
		exchanges[ex] = data[ex]

	for ex in onlyfut:
		exchanges[ex] = []
		for sym in data[ex]:
			if ":USDT" in sym:
				exchanges[ex].append(sym)

	exchdepth = {}
	for ex in exchanges:
		exchdepth[ex] = 1
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
	for ex in exchanges:

		exchange = getattr(ccxt1, ex)()
		exchange.rateLimit = True
		Process(name='worker ' + ex, target=mfun, args=(ex,exchanges[ex],exchdepth[ex],)).start()
