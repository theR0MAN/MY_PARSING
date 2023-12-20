import asyncio
import os
import sys
import ccxt.pro as ccxt  # noqa: E402

names0=['bybit','binance','huobi','bitget' ]

async def poll(names):
	exchanges=[]
	for name in names:
		exchanges.append( getattr(ccxt,name)())
	while True:
		books=[]
		for exchange in exchanges:
			books.append([exchange, await exchange.watch_order_book('BTC/USDT')] )
		yield books
		await asyncio.sleep(1)

async def main():
		async for rez in poll(names0):
			for a,b in rez:
				print(a,b)


asyncio.run(main())