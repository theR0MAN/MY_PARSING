# crypto api key secrets python
# https://docs.waves.exchange/ru/ccxt/#%D0%B7%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B0
# https://docs.ccxt.com/#/ccxt.pro.manual     ccxt.async
# import ccxt.async_support as ccxt
import ccxt.pro as ccxt
import ccxt as ccxt0
import time
import datetime
import asyncio


# print (ccxt.exchanges)
# print (len (ccxt.exchanges))
#


ask0 = {}
bid0 ={}
birza=ccxt0.binance()
markets =birza.load_markets()
cnt=0
for key in markets:
	if  '/USD' in key:
		ask0[key]=0
		bid0[key] = 0
		cnt += 1
print(cnt)
#
#

async def fun1(M, key):
	tm0 = int(time.time())
	while True:
		tm = int(time.time())
		if tm0 != tm:
			tm0 = tm
			orderbook = await M.watch_order_book(key,2)
			# print('BOOK ')
			# print(orderbook )
			bid= orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else 0
			ask= orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else 0
			if (ask0[key] != ask or bid0[key] != bid):
				print(ask, "   ", bid)
				ask0[key] = ask
				bid0[key] = bid

		await asyncio.sleep(0.05)


async def main():
	birza = ccxt.binance ()
	task=asyncio.create_task(fun1(birza, 'BTC/USDT'))
	await task


asyncio.run(main())
