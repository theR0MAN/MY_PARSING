import  asyncio
import time
import os
import datetime
import ccxt.pro as ccxt
from PROJECT.SBOR.my_lib import *

hs=[]
noths=[]
for ex in ccxt.exchanges:
	exchange = getattr(ccxt, ex)()
	if exchange.has['watchOrderBookForSymbols']:
		noths.append(ex)
		print(ex, exchange.has)
	else:
		hs.append(ex)
print(' watchOrderBook',hs)
print('watchOrderBookForSymbols',noths)
# birza='binance'
#
# print( getattr(ccxt, birza)().has)

