# crypto api key secrets python
# https://docs.waves.exchange/ru/ccxt/#%D0%B7%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B0
# https://docs.ccxt.com/#/ccxt.pro.manual     ccxt.async
# import ccxt.async_support as ccxt
import ccxt
import time
import datetime
import asyncio

print (ccxt.exchanges)

print (len (ccxt.exchanges))


# markets =await ccxt.binance().load_markets()
# print(type(markets))



# for key in markets:
# 	if 'BTC/' in key and 'USDT' in key:
# 		print(key)

# etheur1 = markets['BTC/USDT']
# print(etheur1)
# orderbook =binance.fetch_order_book('BTC/USDT')
# print(orderbook)

# quit()
# binance = ccxt.binance()
# instr='BTC/USDT:USDT'
# ask0=0
# bid0=0
# while True:
# 	time.sleep(1)
# 	orderbook = binance.fetch_order_book(instr)
# 	bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
# 	ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
# 	if ask0!= ask or bid0!=bid:
# 		ask0=ask
# 		bid0=bid
# 		print( ask,"   ",bid)



#
#
# binance = ccxt.binance()
# markets = binance.load_markets()
# ask=bid=ask0=bid0={}
# for key in markets:
# 	ask0[key]=0
# 	bid0[key]=0
# 	ask[key]=0
# 	bid[key]=0
#
# while True:
# 	time.sleep(1)
# 	print('погнали')
# 	for key in markets:
# 		orderbook = binance.fetch_order_book(key)
# 		bid[key] = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
# 		ask[key] = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
# 		print(key, '   ', ask[key], "   ", bid[key])
# 		if ask0[key]!= ask[key] or bid0[key]!=bid[key]:
# 			ask0[key]=ask[key]
# 			bid0[key]=bid[key]
# 			# print(key,'   ', ask[key],"   ",bid[key])
#


