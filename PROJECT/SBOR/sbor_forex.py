import MetaTrader5 as mt5
from Sbor_write_lib import Histwrite2
import time
import datetime
import os
import json


def forexsbor(QE):
	putpath = 'G:\\DATA_SBOR'
	startsbor_hour = 4  # 4
	stopsbor_hour = 21  # 21

	def write_compressifo(name, data):
		print('кинуто в очередь ', name)
		QE.put((name, data))

	def getstakan(stakan):
		a = {}
		Ask = 0
		Bid = 0
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
			if asks[0][0] > bids[0][0] and bids[0][0] > 0:
				a['asks'] = asks
				a['bids'] = bids
				Ask = a['asks'][0][0]
				Bid = a['bids'][0][0]
		return [Ask, Bid], {}


	SborFxCUR = Histwrite2(putpath, 'FxCUR', QE)  # ФОРТС
	SborFxMETBR = Histwrite2(putpath, 'FxMETBR', QE)  # американские фьючи

	allnamesst = []
	namesFxCUR = []
	namesFxMETBR = []


	if not mt5.initialize("E:\\AlpariMT5\\terminal64.exe", timeout=30):
		print("initialize() AlpariMT5 failed, error code =", mt5.last_error(), "? once TRY again")
		time.sleep(40)
		if not mt5.initialize("E:\\AlpariMT5\\terminal64.exe", timeout=30):
			print("QUIT!!!!!!!!!!!! initialize() AlpariMT5 failed, error code =", mt5.last_error())
			quit()
		else:
			print('initialize2  AlpariMT5 sucsess')
	else:
		print('initialize1 AlpariMT5 sucsess')
	# ежедневно обновлять список инструментов
	day0 = None
	sec0 = 0
	while True:
		time.sleep(0.005)
		dat = datetime.datetime.utcfromtimestamp(int(time.time()))
		year = dat.year
		day = dat.day
		hour = dat.hour
		sec = dat.second

		if sec0 != sec:
			sec0 = sec
			if startsbor_hour <= stopsbor_hour:
				usl = hour >= startsbor_hour and hour <= stopsbor_hour
			else:  # так как при переходе через 0 может быть ошибочно
				usl = hour >= startsbor_hour or hour <= stopsbor_hour

			if usl:
				if day != day0:
					day0 = day
					symbols = mt5.symbols_get()
					allsym = {}
					for i in symbols:
						sym = i._asdict()
						if sym['name'] in allsym:
							print("fuckingsheat", sym['name'])
						else:
							allsym[sym['name']] = sym
					pth = 'G:\\SYMBOLS_INFO\\FXSYMBOLS_INFO'
					if not os.path.exists(pth):
						os.mkdir(pth)
					pth = pth + '\\' + str(dat.year)
					if not os.path.exists(pth):
						os.mkdir(pth)
					pth = pth + '\\' + str(dat.month)
					if not os.path.exists(pth):
						os.mkdir(pth)
					infoname = pth + '\\' + str(dat.day) + '.roman'
					if not os.path.exists(infoname):
						write_compressifo(infoname,allsym)

					allnamesst = []
					namesFxCUR = []
					namesFxMETBR = []

					t = int(time.time()) + 86400
					timer = time.time()
					print('GO Alpari')
					for sym in allsym:
						sym = allsym[sym]
						if  'Forex\\' in sym['path'] and 'USD' in sym['name']:
							if mt5.market_book_add(sym['name']):
								namesFxCUR.append(sym['name'])
								allnamesst.append(sym['name'])
						if "Spot Metals\\" in sym['path'] or 'Commodity CFD\\' in sym['path']:
							if mt5.market_book_add(sym['name']):
								namesFxMETBR.append(sym['name'])
								allnamesst.append(sym['name'])

					print("размотали имена за", time.time() - timer)

					print(len(allnamesst) )
					print(f' namesFxCUR  {len(namesFxCUR)}')
					print(f' namesFxMETBR  {len(namesFxMETBR)} ')

					count = 0
					namestodel = []
					for sym in allsym:
						sym = allsym[sym]
						if sym['select'] == True:  # 'visible'   'select'
							count += 1
							if sym['name'] not in allnamesst :
								namestodel.append(sym['name'])
								mt5.market_book_release(sym['name'])
								mt5.symbol_select(sym['name'], False)
					print("Выбрано символов", count, "    Лишние символы в количестве", len(namestodel), "  подробней -  ", namestodel)
					if count > 4900:
						print(" ВНИМАНИЕ!  ПРЕГРУЗКА по количеству символов!!!!!!!!! ")

				#  вгоняем стаканы в словарь -чтобы сэкономить 0,2 секунды в среднем на обработке  -чтобы меньшить рассинхрон

				stslovar = {}
				timer = time.time()
				for name in namesFxCUR:
					stslovar[name] = mt5.market_book_get(name)
				for name in namesFxMETBR:
					stslovar[name] = mt5.market_book_get(name)
				# print("получено за", time.time() - timer)

				# обработка словаря на сборщик
				timer = time.time()
				for name in namesFxCUR:
					ab, st = getstakan(stslovar[name])
					SborFxCUR.putter(name, ab, st)
				for name in namesFxMETBR:
					ab, st = getstakan(stslovar[name])
					SborFxMETBR.putter(name, ab, st)
				# print("обработано за" , time.time()-timer )