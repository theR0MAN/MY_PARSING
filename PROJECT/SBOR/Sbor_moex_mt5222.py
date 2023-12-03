import MetaTrader5 as mt5
from Sbor_write_lib import Histwrite2
import time
import datetime
import os
import json


def moexsbor(QE):
	putpath = 'G:\\DATA_SBOR\\'
	startsbor_hour = 4
	stopsbor_hour = 21

	def getstakan(name):
		a = {}
		Ask = 0
		Bid = 0
		stakan = mt5.market_book_get(name)
		if stakan!=None:
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
			if Ask < Bid or Ask == 0 or Bid == 0:
				symbol_info_dict = mt5.symbol_info(name)._asdict()
				Ask = symbol_info_dict['ask']
				Bid = symbol_info_dict['bid']
			if Ask < Bid or Ask == 0 or Bid == 0:
				return [], {}
			else:
				return [Ask, Bid], a
		else:
			symbol_info_dict = mt5.symbol_info(name)._asdict()
			Ask = symbol_info_dict['ask']
			Bid = symbol_info_dict['bid']
			if Ask < Bid or Ask == 0 or Bid == 0:
				return [], {}
			else:
				return [Ask, Bid], {}

	mymarkets = ['FRTS2', 'MOEX2', 'USAFUT', 'CUR', 'CURcross']
	for name in mymarkets:
		if not os.path.exists(putpath + name):
			os.mkdir(putpath + name)

	SborFRTS2 = Histwrite2(putpath, 'FRTS2', QE)  # ФОРТС
	SborMOEX2 = Histwrite2(putpath, 'MOEX2', QE)  # ММВБ
	SborOBLIG = Histwrite2(putpath, 'OBLIG', QE)  # ММВБ  OBLIG
	SborUSAFUT = Histwrite2(putpath, 'USAFUT', QE)  # американские фьючи
	SborCUR = Histwrite2(putpath, 'CUR', QE)  # валютная секция
	SborCURcross = Histwrite2(putpath, 'CURcross', QE)  # из дирректории crossrate
	SborRAW= Histwrite2(putpath, 'RAW', QE)  # из дирректории Indicative continuous

	allnames = []
	namesFRTS2 = []
	namesMOEX2 = []
	namesOBLIG = []
	namesUSAFUT = []
	namesCUR = []
	namesCURcross = []
	namesRAW = []

	if not mt5.initialize("E:\\FinamMT5\\terminal64.exe", timeout=30):
		print("initialize() failed, error code =", mt5.last_error(), "? once TRY again")
		time.sleep(40)
		if not mt5.initialize("E:\\FinamMT5\\terminal64.exe", timeout=30):
			print("QUIT!!!!!!!!!!!! initialize() failed, error code =", mt5.last_error())
			quit()
		else:
			print('initialize2 sucsess')
	else:
		print('initialize1 sucsess')
	# ежедневно обновлять список инструментов
	day0 = None
	names = []
	names2 = []
	while True:
		time.sleep(1)  # не меньше секунды
		dat = datetime.datetime.utcfromtimestamp(int(time.time()))
		year = dat.year
		day = dat.day
		hour = dat.hour
		# print("пишем "  ,time.time())

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

				infoname = str(dat.year) + '-' + str(dat.month) + '-' + str(dat.day)
				if not os.path.exists(putpath + infoname):
					os.mkdir(putpath + infoname)
				if not os.path.exists(putpath + infoname + 'finammt5.json'):
					with open(putpath + infoname + 'finammt5.json', "w") as file:
						json.dump(allsym, file)
				# with open(putpath + infoname + 'finammt5.json', "r") as read_file:
				# 	data = json.load(read_file)
				allnames = []
				namesFRTS2 = []
				namesMOEX2 = []
				namesOBLIG = []
				namesUSAFUT = []
				namesCUR = []
				namesCURcross = []

				t = int(time.time()) + 86400
				for sym in allsym:
					sym = allsym[sym]
					if "MFUT\\" in sym['path'] and sym['expiration_time'] > t:
						if mt5.symbol_select(sym['name'], True):
							mt5.market_book_add(sym['name'])
							namesFRTS2.append(sym['name'])
							allnames.append(sym['name'])
					if "MCT\\Futures\\" in sym['path'] and sym['expiration_time'] > t:
						if mt5.symbol_select(sym['name'], True):
							mt5.market_book_add(sym['name'])
							namesUSAFUT.append(sym['name'])
							allnames.append(sym['name'])
					if "MCUR\\" in sym['path'] and "crossrate" not in sym['path']:
						if mt5.symbol_select(sym['name'], True):
							mt5.market_book_add(sym['name'])
							namesCUR.append(sym['name'])
							allnames.append(sym['name'])
					if "MCUR\\crossrate" in sym['path']:
						if mt5.symbol_select(sym['name'], True):
							mt5.market_book_add(sym['name'])
							namesCURcross.append(sym['name'])
							allnames.append(sym['name'])
					if "Indicative continuous\\" in sym['path']:
						if mt5.symbol_select(sym['name'], True):
							mt5.market_book_add(sym['name'])
							namesRAW.append(sym['name'])
							allnames.append(sym['name'])

					if "MOEX\\" in sym['path'] and (sym['expiration_time'] > t or sym['expiration_time'] == 0):
						if mt5.symbol_select(sym['name'], True):
							mt5.market_book_add(sym['name'])
							allnames.append(sym['name'])
							name = sym['name']
							lnn = len(name)
							perf = name[:2]
							if lnn > 10 and (perf == 'XS' or perf == 'RU' or perf == 'SU'):
								namesOBLIG.append(sym['name'])
							else:
								namesMOEX2.append(sym['name'])

				time.sleep(10)

				count = 0
				namestodel = []
				for sym in allsym:
					sym = allsym[sym]
					if sym['select'] == True:
						count += 1
						if sym['name'] not in allnames:
							namestodel.append(sym['name'])
							mt5.market_book_release(sym['name'])
							mt5.symbol_select(sym['name'], False)
				# print('ALL NAMES  ',allnames)
				print("Выбрано символов", count, "    Лишние символы в количестве", len(namestodel), "  подробней -  ", namestodel)
				if count > 4900:
					print(" ВНИМАНИЕ!  ПРЕГРУЗКА по количеству символов!!!!!!!!! ")

			timer = time.time()
			for name in namesFRTS2:
				AB, st = getstakan(name)
				SborFRTS2.putter(name, AB, st)
			for name in namesUSAFUT:
				AB, st = getstakan(name)
				SborUSAFUT.putter(name, AB, st)
			for name in namesCUR:
				AB, st  = getstakan(name)
				SborCUR.putter(name,  AB, st)
			for name in namesCURcross:
				AB, st  = getstakan(name)
				SborCURcross.putter(name,  AB, st)
			for name in namesRAW:
				AB, st  = getstakan(name)
				SborRAW.putter(name,  AB, st)
			for name in namesMOEX2:
				AB, st  = getstakan(name)
				SborMOEX2.putter(name, AB, st)
			for name in namesOBLIG:
				AB,st = getstakan(name)
				SborOBLIG.putter(name,AB, st)

			print("получено и обработано за", time.time() - timer)
