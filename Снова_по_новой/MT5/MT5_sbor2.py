import MetaTrader5 as mt5
from MAIN.sbor_FUNC import *
import time
import datetime

putpath = 'G:\\DATA_SBOR\\'

startsbor_hour = 4
stopsbor_hour = 20


Sborfrts=Histwrite(putpath,'FRTS')
Sbormoex=Histwrite(putpath,'MOEX')

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
day0 = None
names = []
while True:
	time.sleep(1)  # не меньше секунды
	dat = datetime.datetime.utcfromtimestamp(int(time.time()))
	day = dat.day
	hour=dat.hour

	if startsbor_hour<=stopsbor_hour:
		usl= hour>=startsbor_hour and hour <= stopsbor_hour
	else: # так как при переходе через 0 может быть ошибочно
		usl = hour >= startsbor_hour or hour <= stopsbor_hour

	if usl:
		if day != day0:
			day0 =day
			names = []
			symbols = mt5.symbols_get()
			for sym in symbols:
				sym = sym._asdict()
				usl="RTS\\FORTS\\" in sym['path'] and 'Expired' not in sym['path'] and 'Splice' not in sym['name']
				if usl:
					if mt5.market_book_add(sym['name']):
						names.append(sym['name'])
			time.sleep(3)

		# a = dict()
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
				a= dict()
				# a['a'] = asks[0][0]
				# a['b'] = bids[0][0]
				a['asks'] = asks
				a['bids'] = bids
				Sborfrts.putter(name,a)
				# print(f" Бомбим { name }  {a}")