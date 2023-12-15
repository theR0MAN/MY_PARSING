# crypto api key secrets python
# https://docs.waves.exchange/ru/ccxt/#%D0%B7%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B0
# https://docs.ccxt.com/#/ccxt.pro.manual     ccxt.async
# import ccxt.async_support as ccxt
# https://defillama.com/protocols/Dexes
# https://pypi.org/project/duneapi/
# https://www.coingecko.com/api/documentation
import ccxt.pro as ccxt
import ccxt as ccxt0
import time
import datetime
import asyncio

ask0 = {}
bid0 ={}
count=0

# print (ccxt.exchanges)
# print (len (ccxt.exchanges))
#
async def counter():
	global count
	while True:
		await  asyncio.sleep(1)
		print(count)
		count=0


async def fun1(M, key):
	global count
	tm0 = int(time.time())
	while True:
		tm = int(time.time())
		if tm0 != tm:
			tm0 = tm
			try:
				orderbook = await asyncio.wait_for(M.watch_order_book(key,5),20)
				count+=1
				bid= orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else 0
				ask= orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else 0
				print(key, "   ", ask, "   ", bid)
				if (ask0[key] != ask or bid0[key] != bid):
					# print(key, "   ",ask, "   ", bid)
					ask0[key] = ask
					bid0[key] = bid
			except asyncio.TimeoutError:
				print(' imeoutError',key )
			except:
				print(' ERROR', key)
				
		await asyncio.sleep(0.05)




async def main():
	tasks=[]
	birza = ccxt.bybit()
	ex=ccxt.exchanges
	# print(ex)
	markets = await birza.load_markets()
	# birza.rateLimit=10
	# print(birza.rateLimit)
	# print(birza.has)
	await birza.close()
	# print(markets['ADA/USDC'])
	
	cnt = 0
	for key in markets:
		if '/USDT:' in key and markets[key]['info']['status']=='TRADING':
			cnt += 1
			print(cnt,' YEEE  ',key)

	quit()
	cnt = 0
	for key in markets:
		if '/USD' in key :
			ask0[key] = 0
			bid0[key] = 0
			cnt += 1
	print(cnt)

	n=0
	for key in ask0 : #['AAVEDOWN/USDT','ETH/USDT','LTC/USDT']   ask0     ['PUNDIX/USDT','BCHABC/USDC','NPXS/USDT','NPXS/USDT','AUD/USDC','ADA/USDC','DAI/USDT']
		n+=1
		print(key)
		tasks.append(asyncio.create_task(fun1(birza, key)))
		if n>500:
			break
	task0 = asyncio.create_task(counter())
	await task0
	await asyncio.gather(*tasks)


# asyncio.wait_for()   'status': 'TRADING'

asyncio.run(main())
