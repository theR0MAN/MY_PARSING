import asyncio
import datetime
import time
# import multiprocessing
from multiprocessing import Process
import traceback
import ccxt.pro as ccxt

from PROJECT.SBOR.getlocaldata import rez_dict
from PROJECT.SBOR.my_lib import *


#
# print(' wait 0')
# time.sleep(10)
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

# okx  bitget bitmart bitmex cryptocom  gate  htx kucoin  mexc woo


# 'bitfinex2'

# all= ('bitfinex2','poloniex','bingx', 'whitebit',) #,'whitebit',
# all= ('bingx','bitfinex','bitfinex2','poloniex','kucoinfutures','binanceusdm','whitebit')
# onlyfut=('bybit','binance','phemex',"huobi")
# onlyfut=() #'bybit','binance','huobi','binanceusdm',


# all = ('bitfinex2',)

totalstset=set()
cnnn=0

count = 0
def mfun(ex):

	exchdepth = {}
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
	if ex in exchdepth:
		depth= exchdepth[ex]
	else:depth=1

	errorset=set()
	aliveset=set()


	# huobi  - только фьючи оставить, иначе ошибка
	async def counter():
		global count
		global cnnn
		global totalstset
		count0=0
		tm0 = time.time()
		tmlast = time.time()
		while True:
			tm = time.time()
			await asyncio.sleep(0.05)
			tmlast = time.time()
			if tm0 + 1 <= tm:
				tm0 = tm
				cnnn += 1
				print( len(totalstset))
				if cnnn > 0:
					cnnn = 0
					totalstset = set()
				print(ex,' тормознули на ',round( tm-tmlast,2), ' answers ', count-count0," aliveeset ",len( aliveset) ," erreoeset ",len( errorset), errorset)
				count0=count


	async def poll(exch, symb, stsl,num):
		global count
		global cnnn
		global totalstset
		exchange = getattr(ccxt, exch)()
		tm0 = time.time()
		await asyncio.sleep(stsl)#stsl
		print("START ",exch,symb,"  ",num)

		while True:
			await asyncio.sleep(0.01)
			tm = time.time()
			# dat = datetime.datetime.utcfromtimestamp(tm)
			# if dat.second<=3:
			# 	print(' BREAK TO TIME')
			# 	break
			if tm0 + 0.01 <= tm:
				tm0 = tm
				try:
					timer = time.time()
					# await exchange.throttle(50)
					l=len(symb)
					stset=set()

					while True:
						stk = await exchange.watch_order_book_for_symbols(symb, depth)
						totalstset.add(stk['symbol'])



						# print(l,)

						# dc=dict()
						# if len(stk['asks']) >0 and len(stk['bids']) >0 :
						# 	try:
						# 		Ask = stk['asks'][0][0]
						# 		Bid = stk['bids'][0][0]
						# 		if Ask > 0 and Bid > 0 and Ask >Bid:
						# 			dc['asks']=stk['asks']
						# 			dc['bids'] = stk['bids']
						# 			if stk['timestamp'] != None:
						# 				dc['timestamp'] = stk['timestamp'] / 1000
						# 			else:
						# 				dc['timestamp'] = None
						# 			dc['zad']= time.time() - timer
						# 			myredput(symb+'*'+exch,dc)
						# 			count+=1
						# 	except:
						# 		print(exch," какая то херь в криптомашине с",symb )

					# aliveset.add(exch+symb)
					# if exch+symb in errorset:
					# 	print('ALIVE ',exch+symb)
					# 	errorset.remove(exch+symb)

				except Exception:
					await  exchange.close()
					await asyncio.sleep(1)
					# errorset.add(exch+symb)
					traceback.print_exc()
					# if exch+symb in aliveset:
						# print('DEAD ',exch+symb)
						# aliveset.remove(exch+symb)

	async def main(ex):
		asyncio.create_task(counter())
		day0=-1
		vorksymbols=set()
		while True:
			await  asyncio.sleep(5)
			# раз в день проверять обновления символов
			dat = datetime.datetime.utcfromtimestamp(time.time())
			day=dat.day
			mnt=dat.minute
			if day0!=day and mnt>3:  #day0!=day and mnt>3
				print('day0!=day and mnt>3 POGNALI')
				day0 = day
				dct=myload('G:\\SYMBOLS_INFO\\KRIPTASYMBOLS_INFO\\log.roman')
				if ex in dct:
					symbols=dct[ex]
					# symbols = ['UNI/USDT:USDT', 'ARB/USDT:USDT', 'NEAR/USDT:USDT', 'MKR/USDT:USDT', 'DOT/USDT:USDT', 'SUI/USDT:USDT', 'FTM/USDT:USDT', 'DYM/USDT:USDT',
					# 		   'AGIX/USDT:USDT', 'SEI/USDT:USDT', 'MEME/USDT:USDT', 'INJ/USDT:USDT' ]
					# symbols=['OM/USDT:USDT', 'KNC/USDT:USDT', 'LUNA/USDT:USDT', 'GAL/USDT:USDT', 'BAL/USDT:USDT']

					print(f" {ex} get symbols {len(symbols)} ")
					time.sleep(2)
					stsl = 0
					num = 0
					symsp=[]
					for sym in symbols:
						if sym not in vorksymbols:
							vorksymbols.add(sym)
							num+=1
							stsl+=2
							print(ex,' PUSK ',sym)
							symsp.append(sym)
					if len (symsp)>0:
						asyncio.create_task(poll(ex, symsp, stsl,num))
				else:
					print(ex,'ZJOPA')
	asyncio.run(main(ex))


if __name__ == "__main__":


	# all = ('bingx', 'whitebit', 'bitfinex2','poloniex',)
	# onlyfut = ('bybit', 'binance', 'huobi', 'binanceusdm',)
	all = ()
	onlyfut = ('okx',)
	# all = ('whitebit','bingx',)
	# onlyfut = ('huobi',  'binanceusdm', 'bybit', )
	rez=rez_dict(20, 50, all, onlyfut, True)

	dat = datetime.datetime.utcfromtimestamp(time.time())
	day00 = dat.day
	for ex in rez:
		exchange = getattr(ccxt, ex)()
		exchange.rateLimit = True
		Process(name='worker' + ex, target=mfun, args=(ex,)).start()
	print('ZAEBUBA')


	while True:
		time.sleep(10)
		dat = datetime.datetime.utcfromtimestamp(time.time())
		day = dat.day
		mnt = dat.minute
		if day00 != day:  # and mnt>1
			day00 = day
			rez_dict(20, 50, all, onlyfut, True)

#
#   File "C:\Users\milro\AppData\Roaming\Python\Python39\site-packages\ccxt\base\exchange.py", line 2982, in market_symbols
#     raise BadRequest(self.id + ' symbols must be of the same type, either ' + marketType + ' or ' + market['type'] + '.')
# ccxt.base.errors.BadRequest: binance symbols must be of the same type, either swap or future.
#






