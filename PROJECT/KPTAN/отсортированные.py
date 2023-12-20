import asyncio
import os
import sys
import ccxt.pro as ccxt  # noqa: E402
import traceback
from PROJECT.my_lib import *

# exshanges=['poloniexfutures']
# exshanges=['binance','bybit','mexc','gate','huobi','whitebit','poloniexfutures','okx']
# symbols=["BTC/USDT:USDT"]    #,"LTC/USDT:USDT"
godset = set()
exchanges = {}
exchdepth = {}
data = myload('Frez')
# {'bitopro', 'gate', 'okx', 'whitebit', 'hollaex', 'cryptocom', 'upbit', 'kraken', 'bitrue', 'probit', 'ascendex', 'gateio', 'bybit', 'kucoin', 'poloniex', 'huobi', 'bingx', 'kucoinfutures', 'binance', 'mexc', 'bitfinex2', 'bitmart', 'blockchaincom', 'bitmex', 'bitfinex', 'phemex', 'wazirx', 'binanceusdm', 'bitget', 'poloniexfutures'}
otborex= ('binance', 'bitfinex2', 'ascendex', 'bitmex', 'hollaex', 'kucoinfutures', 'poloniexfutures', 'okx', 'phemex',  'bitopro',  'cryptocom', 'binanceusdm', 'bitfinex', 'upbit', 'whitebit', 'gateio', 'wazirx', 'kraken', 'bitget', 'blockchaincom', 'bybit', 'gate', 'bitmart', 'probit', 'mexc', 'poloniex', 'kucoin', 'bingx')

 # с таймштампом -{'blockchaincom', 'ascendex', 'phemex', 'gate', 'kucoinfutures', 'bitmex', 'mexc', 'wazirx', 'bitmart', 'kraken', 'bybit', 'poloniexfutures', 'poloniex', 'binanceusdm', 'hollaex', 'kucoin', 'upbit', 'bitopro', 'bitget', 'binance', 'okx', 'cryptocom', 'gateio'}

# print(len(otborex))
# quit()
for ex in otborex:
	exchanges[ex] = []
	exchdepth[ex] = 1
	for sym in data[ex]['futures']:
		exchanges[ex].append(sym)
		break
	for sym in data[ex]['spot']:
		exchanges[ex].append(sym)
		break
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


# huobi  - только фьючи оставить, иначе ошибка

async def poll(exch, symb, depth):
	exchange = getattr(ccxt, exch)()
	while True:
		try:
			stk=await exchange.watch_order_book(symb, depth)
			# print(exch )
			# godset.add(exch)
			try:
				# print(f" {exch}  {symb}   Ask= {stk['asks'][0][0]}  Bid= {stk['bids'][0][0]}  timestamp= {stk['timestamp']}")
				if stk['timestamp']!=None:
					godset.add(exch)
				print(godset)
				await asyncio.sleep(3)
			except:
				print(f" BADDDD  {exch}  {symb}   Ask= {stk['asks']}  Bids= {stk['bids']}  timestamp= {stk['timestamp']}")
			await asyncio.sleep(2)

			# if len (stk['asks']) >0 and len (stk['bids']>0):
			# 	print(f" {exch}  {symb}   Ask= {stk['asks'][0][0]}  Bid= {stk['bids'][0][0]}")
			# else:
			# 	print(f" BADDDD  {exch}  {symb}   Ask= {stk['askss']}  Bids= {stk['bids']}")
			# await asyncio.sleep(2)

		except Exception:
			await  exchange.close()
			await asyncio.sleep(1)
			print(exch, symb, "  ERROR")
			traceback.print_exc()


async def main():
	tasks = []
	for ex in exchanges:
		for sym in exchanges[ex]:
			tasks.append(poll(ex, sym, exchdepth[ex]))

	await asyncio.gather(*tasks)


asyncio.run(main())