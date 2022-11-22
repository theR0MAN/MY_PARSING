import MetaTrader5 as mt5
from MAIN.sbor_FUNC import *
import json
from platform import system
from multiprocessing import Process
import time
import os
import lzma
import datetime



putpath = 'G:\\DATA_SBOR\\MOEX'

if not mt5.initialize("G:\\Открытие ФОРТС\\terminal64.exe", timeout=30):
	print("initialize() failed, error code =", mt5.last_error(),"? once TRY again")
	time.sleep(10)
	if not mt5.initialize("G:\\Открытие ФОРТС\\terminal64.exe", timeout=30):
		print("QUIT!!!!!!!!!!!! initialize() failed, error code =", mt5.last_error())
		quit()
	else:
		print('initialize2 sucsess')
else:
	print('initialize1 sucsess')
# ежедневно обновлять список инструментов
day0 = -1
names = []
while True:
	time.sleep(1)
	dat = datetime.datetime.utcfromtimestamp(int(time.time()))
	day = dat.day
	if day != day0:
		day0 =day
		names = []
		symbols = mt5.symbols_get()
		for sym in symbols:
			sym = sym._asdict()
			if "RTS\\FORTS\\" in sym['path'] and 'Expired' not in sym['path'] and 'Splice' not in sym[
				'name']:
				if mt5.market_book_add(sym['name']):
					names.append(sym['name'])
		time.sleep(3)

	a = dict()
	for name in names:
		stakan = mt5.market_book_get(name)
		asks = []
		bids = []
		for i in stakan:
			i = i._asdict()
			if i['type'] == 1:
				asks.append((i['price'], i['volume']))
			if i['type'] == 2:
				bids.append((i['price'], i['volume']))
		asks.reverse()
		if len(asks) > 0 and len(bids) > 0:
			a[name] = dict()
			a[name]['a'] = asks[0][0]
			a[name]['b'] = bids[0][0]
			a[name]['asks'] = asks
			a[name]['bids'] = bids
	if len(a)>0:
		HISTWRITER(putpath, a)

