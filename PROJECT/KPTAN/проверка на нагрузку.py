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
# kvo birz  53
# 122 {'BTC': 82, 'ETH': 77, 'XRP': 64, 'LTC': 60, 'EOS': 58, 'SOL': 55, 'DOGE': 55, 'ETC': 54, 'MATIC': 52, 'ADA': 52, 'LINK': 52, 'AVAX': 51, 'APE': 50, 'DOT': 49, 'TRX': 49, 'UNI': 48, 'ATOM': 48, 'BCH': 48, 'XLM': 47, 'SAND': 47, 'AXS': 46, 'FIL': 45, 'APT': 44, 'FTM': 44, 'ARB': 44, 'NEAR': 44, 'BNB': 43, 'AAVE': 42, 'SHIB': 42, 'CRV': 42, 'CHZ': 42, 'MANA': 41, 'XTZ': 41, 'OP': 41, 'BLUR': 40, 'FET': 40, 'ALGO': 40, 'SUI': 40, 'COMP': 40, 'SNX': 40, 'SUSHI': 39, 'ICP': 39, 'YFI': 39, 'MKR': 39, 'WOO': 39, 'RNDR': 39, 'LRC': 39, 'GRT': 38, 'DYDX': 38, 'WAVES': 38, 'GALA': 38, 'LDO': 38, 'MASK': 38, 'BAT': 38, 'ZRX': 37, 'NEO': 37, 'EGLD': 37, '1INCH': 37, 'IMX': 37, 'ENS': 36, 'INJ': 36, 'WLD': 36, 'KSM': 36, 'JASMY': 35, 'GMT': 35, 'FLOW': 35, 'ENJ': 35, 'OMG': 34, 'TIA': 34, 'TRB': 34, 'BAND': 34, 'USDC': 34, 'MINA': 34, 'THETA': 34, 'KNC': 34, 'SSV': 34, 'ZIL': 33, 'XMR': 33, 'GMX': 33, 'ACH': 33, 'BNT': 33, 'AGIX': 33, 'GAL': 33, 'KAVA': 33, 'ID': 32, 'CAKE': 32, 'FLOKI': 32, 'HBAR': 32, 'STORJ': 32, 'STG': 32, 'BIGTIME': 32, 'PEPE': 32, 'ONE': 32, 'YGG': 32, 'MEME': 32, 'REN': 32, 'ORDI': 32, 'AGLD': 32, 'ACE': 32, 'VET': 32, 'LPT': 31, 'OGN': 31, 'ZEC': 31, 'SEI': 31, 'KLAY': 31, 'PYTH': 31, 'STX': 31, 'QTUM': 31, 'RSR': 31, 'BAL': 31, 'ETHW': 30, 'ANKR': 30, 'LUNC': 30, 'MAGIC': 30, 'RVN': 30, 'PEOPLE': 30, 'RDNT': 30, 'QNT': 30, 'OCEAN': 30, 'BICO': 30, 'AR': 30, 'WAXP': 30}
# all exc 28 {'gate': 264, 'gateio': 264, 'okx': 244, 'binance': 241, 'bitget': 231, 'bingx': 229, 'bybit': 224, 'phemex': 216, 'bitmart': 214, 'huobi': 211, 'htx': 211, 'mexc': 149, 'bitcoincom': 144, 'hitbtc': 144, 'whitebit': 135, 'ascendex': 132, 'binanceusdm': 122, 'kucoinfutures': 120, 'bitrue': 119, 'kucoin': 119, 'bitfinex2': 109, 'wazirx': 105, 'coinex': 102, 'cryptocom': 101, 'poloniex': 94, 'bequant': 77, 'probit': 76, 'bitfinex': 65}

# futures  21 {'gate': 142, 'gateio': 142, 'okx': 132, 'binanceusdm': 122, 'binance': 122, 'kucoinfutures': 120, 'mexc': 120, 'bybit': 118, 'phemex': 117, 'bitget': 117, 'bingx': 109, 'coinex': 102, 'bitmart': 98, 'htx': 92, 'huobi': 92, 'ascendex': 49, 'bitfinex2': 44, 'whitebit': 32, 'bitcoincom': 27, 'hitbtc': 27, 'bequant': 21}
# onlyspot 7 {'kucoin': 119, 'bitrue': 119, 'wazirx': 105, 'cryptocom': 101, 'poloniex': 94, 'probit': 76, 'bitfinex': 65}
# option markets   {'gateio', 'gate'}
otborex= ( 'bybit',)
# 'bybit','binance','poloniex',
# print(len(otborex))
# quit()
# 'bybit' 100+100
# 'binance'100
count=0
limits=300
for ex in otborex:
	exchanges[ex] = []
	exchdepth[ex] = 1
	counts = 0
	for sym in data[ex]:
		exchanges[ex].append(sym)
		counts+=1
		if counts>= limits:
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



async def poll(exch, symb, depth,stsl,num):
	global count
	exchange = getattr(ccxt, exch)()
	tm0 = time.time()
	await asyncio.sleep(stsl)
	print("START ",exch,symb,"  ",num)
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

	task0=counter()
	tasks = []
	for ex in exchanges:
		exchange = getattr(ccxt, ex)()
		exchange.rateLimit = 10
		stsl = 0
		num = 0
		for sym in exchanges[ex]:
			num+=1
			stsl+=1
			tasks.append(poll(ex, sym, exchdepth[ex],stsl,num))

	await asyncio.gather(*tasks,task0)


asyncio.run(main())