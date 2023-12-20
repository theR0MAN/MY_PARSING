import asyncio
import os
import sys
import ccxt.pro as ccxt  # noqa: E402


async def poll():
	exchange = ccxt.binance()
	while True:
		yield await exchange.watch_order_book('BTC/USDT')
		# await asyncio.sleep(exchange.rateLimit / 1000)
		await asyncio.sleep(1)


async def main():
	async for orderbook in poll():
		print(orderbook['bids'][0], orderbook['asks'][0])


asyncio.run(main())
