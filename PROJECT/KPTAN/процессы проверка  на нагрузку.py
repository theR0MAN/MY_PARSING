import asyncio
import os
import sys
import time
import datetime
from multiprocessing import Process,Queue
from PROJECT.SBOR.Sbor_write_lib import Compress
from  PROJECT.SBOR.Sbor_write_lib import Histwrite2
import ccxt.pro as ccxt1  # noqa: E402
import traceback
from PROJECT.my_lib import *
from PROJECT.KPTAN.SBOR.getdatfile import rez_dict
QE = Queue()
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


count=0
def mfun(ex,symbols,depth,QE):
	ccxt=ccxt1
	errorset=set()
	aliveset=set()
	print(f" {ex} get symbols {len(symbols)} ")
	time.sleep(2)

	# huobi  - только фьючи оставить, иначе ошибка
	async def counter():
		global count
		insidecount=0
		count0=0
		tm0 = time.time()
		tmlast = time.time()
		while True:
			tm = time.time()
			await asyncio.sleep(0.05)
			tmlast = time.time()
			if tm0 + 1 <= tm:
				tm0 = tm
				insidecount+=1
				print(ex, ' тормознули на ', round(tm - tmlast, 2), ' answers ', count - count0, " aliveeset ", len(aliveset), " erreoeset ", len(errorset), errorset)
				# if  insidecount>5:
				# 	insidecount=0
				# 	print(ex,' тормознули на ',round( tm-tmlast,2), ' answers ', count-count0," aliveeset ",len( aliveset) ," erreoeset ",len( errorset), errorset)
				count0 = count


	async def poll(Sbor,exch, symb, depth,stsl,num):
		global count
		exchange = getattr(ccxt, exch)()
		tm0 = time.time()
		await asyncio.sleep(stsl)
		# print("START ",exch,symb,"  ",num)
		while True:
			await asyncio.sleep(0.05)
			tm = time.time()
			if tm0 + 1 <= tm:
				tm0 = tm
				try:
					timer = time.time()
					stk=await exchange.watch_order_book(symb, depth)
					zaderzka= timer- time.time()
					count+=1
					tm = time.time()
					aliveset.add(exch+symb)
					if exch+symb in errorset:
						# print('ALIVE ',exch+symb)
						errorset.remove(exch+symb)
					Ask= stk['asks'][0][0]
					Bid= stk['bids'][0][0]
					timestamp =stk['timestamp'] /1000
					if Ask==0 or Bid==0 or Ask<Bid:
						askbid=[0,0]
					else:
						askbid=[Ask,Bid,timestamp,zaderzka]
					Sbor.putter(symb,askbid,{})

				except Exception:
					await  exchange.close()
					await asyncio.sleep(1)
					errorset.add(exch+symb)
					if exch+symb in aliveset:
						# print('DEAD ',exch+symb)
						aliveset.remove(exch+symb)
					# print( "  ERRORset ",errorset)
					# traceback.print_exc()
	async def main(ex):
		putpath = 'G:\\DATA_SBOR\\KRIPTA'
		Sbor = Histwrite2(putpath, ex, QE)  # ФОРТС
		task0=counter()
		tasks = []
		stsl = 0
		num = 0
		for sym in symbols:
			num+=1
			stsl+=2
			tasks.append(poll(Sbor,ex, sym, depth,stsl,num))
		await asyncio.gather(*tasks,task0)

	asyncio.run(main(ex))


if __name__ == "__main__":
	Process(target=Compress, args=(QE,)).start()
	day0=0
	proc = []
	while True:
		dat=datetime.datetime.utcfromtimestamp(time.time())
		day = dat.day
		hr=dat.hour
		mn=dat.minute
		if day0!=day and mn>1:
			print(' NEW DAY')
			day0=day
			data = rez_dict (False,30,40,50)
			exchanges = {}
			retryset=set()

			# all= ('bingx','bitfinex','bitfinex2','poloniex','kucoinfutures','binanceusdm','whitebit')
			# onlyfut=('bybit','binance','phemex',"huobi")
			# all = ('bingx', 'whitebit','bitfinex2',)
			# onlyfut = ('bybit', 'binance', 'huobi', 'binanceusdm',)
			all = ( 'bitfinex2',)
			onlyfut = ()

			while True:
				for ex in all:
					if ex not in data:
						data = rez_dict(True,30, 40, 50)
						print('retry cycle ',ex)
						continue
				for ex in onlyfut:
					if ex not in data:
						data = rez_dict(True,30, 40, 50)
						print('retry cycle ', ex)
						continue
				print('its allright')
				break

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

			if len(proc) > 0:
				print(' CLOSE PROC')
				for p in proc:
					p.terminate()
					p.kill()
					p.close()
				proc = []
			time.sleep(5)
			for ex in exchanges:
				getattr(ccxt1, ex)().rateLimit = True
				proc.append(Process(name='worker ' + ex, target=mfun, args=(ex,exchanges[ex],exchdepth[ex],QE,)))
			for p in proc:
				p.start()
				print(' start PROC ', p)
		time.sleep(5)


