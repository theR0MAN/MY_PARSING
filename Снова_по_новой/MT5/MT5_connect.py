import MetaTrader5 as mt5
import time

# from collections import namedtuple
# import pandas as pd
# time.sleep(20)
if not mt5.initialize( "G:\\Открытие ФОРТС\\terminal64.exe",timeout=30 ) :
	print("initialize() failed, error code =", mt5.last_error())
	quit()


symbol_info=mt5.symbol_info("RUCBTR5Y")
# if symbol_info!=None:
# выведем данные о терминале как есть
print(symbol_info)

gg=mt5.market_book_add ('RUCBTR5Y')
print('gg ',gg)
time.sleep(3)

stakan=mt5.market_book_get( 'RUCBTR5Y')

asks=[]
bids=[]
for i in stakan:
	i=i._asdict()
	if i['type']==1:
		asks.append((i['price'],i['volume']))
	if i['type']==2:
		bids.append((i['price'], i['volume']))
asks.reverse()
print(asks)
print(bids)

print(f'ask {asks[0][0]}  volask {asks[0][1]}  ')
print(f'bid {bids[0][0]}  volbid {bids[0][1]}  ')


# mt5.shutdown()


