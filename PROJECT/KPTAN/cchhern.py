import ccxt

import ccxt.pro as ccxtpro
from asyncio import run
# if exchange.has['watchOrderBookForSymbols']:

# async def main():
# 	exchange = ccxtpro.kraken({'newUpdates': True})
# 	while True:
# 		orderbook = await exchange.watch_order_book('BTC/USD')
# 		print(orderbook['asks'][0], orderbook['bids'][0])
# 	await exchange.close()

# run(main())
# ccxtpro.binance().throttle
# https://gitmemories.com/ccxt/ccxt/issues/14628

# {
#     'bids': [
#         [ price, amount ], // [ float, float ]
#         [ price, amount ],
#         ...
#     ],
#     'asks': [
#         [ price, amount ],
#         [ price, amount ],
#         ...
#     ],
#     'symbol': 'ETH/BTC', // a unified market symbol
#     'timestamp': 1499280391811, // Unix Timestamp in milliseconds (seconds * 1000)
#     'datetime': '2017-07-05T18:47:14.692Z', // ISO8601 datetime string with milliseconds
#     'nonce': 1499280391811, // an increasing unique identifier of the orderbook snapshot
# }

# okcoin = ccxt.okcoin()
# markets = okcoin.load_markets()
# print(okcoin.id, markets)

# if exchange.has
