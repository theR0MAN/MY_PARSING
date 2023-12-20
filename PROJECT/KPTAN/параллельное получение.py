import asyncio
import os
import sys
import ccxt.pro as ccxt  # noqa: E402
import traceback
from PROJECT.my_lib import *
# exshanges=['poloniexfutures']
# exshanges=['binance','bybit','mexc','gate','huobi','whitebit','poloniexfutures','okx']
# symbols=["BTC/USDT:USDT"]    #,"LTC/USDT:USDT"
godset=set()
exchanges={}
exchdepth={}
data=myload('Frez')

# {'binance', 'bitfinex2', 'ascendex', 'bitmex', 'hollaex', 'kucoinfutures', 'poloniexfutures', 'okx', 'phemex', 'bitrue', 'bitopro', 'huobi', 'cryptocom', 'binanceusdm', 'bitfinex', 'upbit', 'whitebit', 'gateio', 'wazirx', 'kraken', 'bitget', 'blockchaincom', 'bybit', 'gate', 'bitmart', 'probit', 'mexc', 'poloniex', 'kucoin', 'bingx'}
for ex in data:
	exchanges[ex]=[]
	exchdepth[ex] =1
	for sym in data[ex]['futures']:
		exchanges[ex].append(sym)
		break
	for sym in data[ex]['spot']:
		exchanges[ex].append(sym)
		break
exchdepth['kucoinfutures']=20
exchdepth['kraken']=10
exchdepth['kucoin']=20
exchdepth['bitfinex2']=25
exchdepth['bitmex']=None
exchdepth['bitopro']=None #5
exchdepth['bitfinex']=25
exchdepth['bingx']= 20
exchdepth['poloniexfutures']= 5
exchdepth['huobi']=20
# exchdepth['htx']=None#20
exchdepth['binanceusdm']=5
exchdepth['binance']=5
exchdepth['coinex']=None
# require API
del (exchanges['coinbasepro'])
del (exchanges['coinbaseprime'])


# NO LOADED :
del (exchanges['bitcoincom'])
del (exchanges['bequant'])
del (exchanges['hitbtc'])
del (exchanges['htx'])


async def poll(exch,symb,depth):
	exchange = getattr(ccxt,exch)()
	while True:
		try:
			await exchange.watch_order_book(symb, depth)
			# print(exch )
			godset.add(exch)
			print(godset)
			await asyncio.sleep(2)

		except Exception:
			await  exchange.close()
			await asyncio.sleep(1)
			print( exch,symb,"  ERROR")
			traceback.print_exc()



async def main():
	tasks=[]
	for ex in exchanges:
		for sym in exchanges[ex]:
			tasks.append(poll(ex,sym,exchdepth[ex]))
			
	await asyncio.gather(*tasks)


asyncio.run(main())