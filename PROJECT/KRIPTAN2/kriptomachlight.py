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



	async def poll(exch, symb):
		global count
		exchange = getattr(ccxt, exch)()
		print("START ",exch,symb)

		while True:
			# await asyncio.sleep(0.01)

			try:
				timer = time.time()
				stk=await exchange.watch_order_book_for_symbols(symb, depth)
				print(stk)


			except Exception:
				print('pizdec')
				traceback.print_exc()
				await  exchange.close()
				# await asyncio.sleep(1)

	async def main(ex):
		# asyncio.create_task(counter())
		day0=-1
		vorksymbols=set()
		# while True:
		# await  asyncio.sleep(5)
		# раз в день проверять обновления символов
		dat = datetime.datetime.utcfromtimestamp(time.time())
		day=dat.day
		mnt=dat.minute
		if day0!=day and mnt>2:  #day0!=day and mnt>3
			# print('day0!=day and mnt>3 POGNALI')
			day0 = day
			# dct=myload('G:\\SYMBOLS_INFO\\KRIPTASYMBOLS_INFO\\log.roman')
			# if ex in dct:
			symbols = ['UNI/USDT:USDT', 'ARB/USDT:USDT', 'NEAR/USDT:USDT', 'MKR/USDT:USDT', 'DOT/USDT:USDT','SUI/USDT:USDT', 'FTM/USDT:USDT', 'DYM/USDT:USDT', 'AGIX/USDT:USDT', 'SEI/USDT:USDT', 'MEME/USDT:USDT', 'INJ/USDT:USDT',]

			print(f" {ex} get symbols {len(symbols)} ")
			asyncio.create_task(poll(ex, symbols))
					# print(ex,'ZJOPA')
	asyncio.run(main(ex))


mfun('binance')


#
# async def main():
# 	ex = 'binance'
# 	symbols = ['BTC/USDT:USDT', 'BTC/USDT:USDT-240329', 'BTC/USDT:USDT-240628', 'ETH/USDT:USDT', 'ETH/USDT:USDT-240329', 'ETH/USDT:USDT-240628', 'AXS/USDT:USDT', 'LINK/USDT:USDT',
# 			   'UNI/USDT:USDT', 'ARB/USDT:USDT', 'NEAR/USDT:USDT', 'MKR/USDT:USDT', 'DOT/USDT:USDT', 'APT/USDT:USDT', 'FIL/USDT:USDT', 'DOGE/USDT:USDT', 'APE/USDT:USDT',
# 			   'AVAX/USDT:USDT', 'EOS/USDT:USDT', 'LTC/USDT:USDT', 'ETC/USDT:USDT', 'MATIC/USDT:USDT', 'XRP/USDT:USDT', 'TRX/USDT:USDT', 'SOL/USDT:USDT', 'ADA/USDT:USDT',
# 			   'GRT/USDT:USDT', 'ICP/USDT:USDT', 'SAND/USDT:USDT', 'CRV/USDT:USDT', 'AAVE/USDT:USDT', 'BLUR/USDT:USDT', 'GALA/USDT:USDT', 'FET/USDT:USDT', 'SUSHI/USDT:USDT',
# 			   'SNX/USDT:USDT', 'STRK/USDT:USDT', 'ATOM/USDT:USDT', 'TIA/USDT:USDT', 'JUP/USDT:USDT', 'EGLD/USDT:USDT', 'XLM/USDT:USDT', 'STG/USDT:USDT', 'COMP/USDT:USDT',
# 			   'SUI/USDT:USDT', 'FTM/USDT:USDT', 'DYM/USDT:USDT', 'AGIX/USDT:USDT', 'SEI/USDT:USDT', 'MEME/USDT:USDT', 'INJ/USDT:USDT', 'RNDR/USDT:USDT', 'ZETA/USDT:USDT',
# 			   'MANTA/USDT:USDT']
# 	print(f" {ex} get symbols {len(symbols)} ")
# 	day0=-1
# 	while True:
# 		await  asyncio.sleep(5)
# 		time.sleep(2)
# 		stsl = 0
# 		num = 0
# 		asyncio.create_task(poll(ex, symbols, stsl,num))
#
#
# asyncio.run(main())











