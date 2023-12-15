# import ccxt.async_support as ccxt
# ccxt.async
import ccxt
import asyncio
import time

now = lambda: time.time()
start = now()


async def getData(exchange, symbol):
	data = {}  # Used to store ticker and depth information


# Get ticker information
tickerInfo = await exchange.fetch_ticker(symbol)
# Get depth information
depth = {}
# Get depth information
exchange_depth = await exchange.fetch_order_book(symbol)
# Get asks, bids minimum 5, maximum 5 information
asks = exchange_depth.get('asks')[:5]
bids = exchange_depth.get('bids')[:5]
depth['asks'] = asks
depth['bids'] = bids

data['ticker'] = tickerInfo
data['depth'] = depth

return data


def main():
	# Instantiating the market
	exchanges = [ccxt.binance(), ccxt.bitfinex2(), ccxt.okex(), ccxt.gdax()]
	# Trading pair
	symbols = ['BTC/USDT', 'BTC/USD', 'BTC/USDT', 'BTC/USD']

	tasks = []
	for i in range(len(exchanges)):
		task = getData(exchanges[i], symbols[i])
		tasks.append(asyncio.ensure_future(task))

	loop = asyncio.get_event_loop()
	loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
	main()
	print('Run Time: %s' % (now() - start))