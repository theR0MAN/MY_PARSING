import MetaTrader5 as mt5
from Sbor_write_lib import Histwrite2
import time
import datetime
import os
import json

def moexsbor(QE):
	sboroblig=False    # собирать облигации
	putpath = 'G:\\DATA_SBOR\\MOSCOWEXCH\\FINAM'
	startsbor_hour = 4# 4
	stopsbor_hour = 21# 21
	# печатать инструменты с пустыми стаканами
	def write_compressifo(name, data):
		print( 'кинуто в очередь ',name)
		QE.put((name,data))

	def getstakan(stakan):
		a = {}
		Ask=0
		Bid=0
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
			if asks[0][0] > bids[0][0] and bids[0][0]>0 :
				a['asks'] = asks
				a['bids'] = bids
				Ask = a['asks'][0][0]
				Bid = a['bids'][0][0]
		return [Ask,Bid],a

	def getAB(data):
		symbol_info_dict = data._asdict()
		Ask = symbol_info_dict['ask']
		Bid = symbol_info_dict['bid']
		if Ask<Bid:
			Ask=0
			Bid=0
		return [Ask, Bid], {}
	# mymarkets=['FRTS2','MOEX2','USAFUT','CUR','CURcross',"RAW"]
	# for name in mymarkets:
	# 	if not os.path.exists(putpath + name ):
	# 		os.mkdir(putpath + name )

	SborFRTS2= Histwrite2(putpath, 'FRTS2',QE) #  ФОРТС
	SborUSAFUT = Histwrite2(putpath, 'USAFUT', QE)  # американские фьючи
	SborCUR= Histwrite2(putpath, 'CUR', QE)  #  валютная секция
	SborMOEX2 = Histwrite2(putpath, 'MOEX2',QE)  #   ММВБ
	if sboroblig:
		SborOBLIG= Histwrite2(putpath, 'OBLIG', QE)  #   ММВБ  OBLIG
	SborCURcross= Histwrite2(putpath, 'CURcross', QE) # из дирректории crossrate
	SborRAW = Histwrite2(putpath, 'RAW', QE)  # сырье

	allnamesst = []
	allnamesab= []
	namesFRTS2 = []
	namesMOEX2 = []
	namesOBLIG  = []
	namesUSAFUT = []
	namesCUR = []
	namesCURcross = []
	namesRAW = []

	if not mt5.initialize("E:\\FinamMT5\\terminal64.exe", timeout=30):
		print("initialize() failed, FinamMT5 error code =", mt5.last_error(), "? once TRY again")
		time.sleep(40)
		if not mt5.initialize("E:\\FinamMT5\\terminal64.exe", timeout=30):
			print("QUIT!!!!!!!!!!!! FinamMT5 initialize() failed, error code =", mt5.last_error())
			quit()
		else:
			print('initialize2  FinamMT5 sucsess')
	else:
		print('initialize1 FinamMT5 sucsess')
	# ежедневно обновлять список инструментов
	day0 = None
	sec0=0
	while True:
		time.sleep(0.005)
		dat = datetime.datetime.utcfromtimestamp(int(time.time()))
		year=dat.year
		day = dat.day
		hour = dat.hour
		sec=dat.second
		if sec0!= sec:
			sec0=sec
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
					pth = putpath + '\\ASYMBOLS_INFO'
					if not os.path.exists(pth):
						os.mkdir(pth)
					pth=pth +'\\'+ str(dat.year)
					if not os.path.exists(pth):
						os.mkdir(pth)
					pth=pth+ '\\'+ str(dat.month)
					if not os.path.exists(pth):
						os.mkdir(pth)
					infoname = pth+'\\'+str(dat.day) + '.roman'
					if not os.path.exists(infoname ):
						write_compressifo(infoname,allsym)

					allnamesst=[]
					allnamesab = []

					namesFRTS2 = []
					namesMOEX2 = []
					namesOBLIG = []
					namesUSAFUT = []
					namesCUR = []
					namesCURcross = []
					namesRAW = []

					t = int(time.time()) + 86400
					timer = time.time()
					print('GO')
					for sym in allsym:
						sym = allsym[sym]
						if "MFUT\\" in sym['path'] and sym['expiration_time']>t :
							if mt5.market_book_add(sym['name']):
								namesFRTS2.append(sym['name'])
								allnamesst.append(sym['name'])
						if "MCT\\Futures\\" in sym['path']and sym['expiration_time']>t :
							if mt5.market_book_add(sym['name']):
								namesUSAFUT.append(sym['name'])
								allnamesst.append(sym['name'])
						if "MCUR\\" in sym['path'] and "crossrate" not in sym['path']:
							if mt5.market_book_add(sym['name']):
								namesCUR.append(sym['name'])
								allnamesst.append(sym['name'])
						if "MOEX\\" in sym['path'] and ( sym['expiration_time']>t or sym['expiration_time']==0 ) :
							name = sym['name']
							lnn = len(name)
							perf = name[:2]
							if  lnn > 10 and (perf == 'XS' or perf == 'RU' or perf == 'SU'):
								if sboroblig:
									if mt5.market_book_add(sym['name']):
										allnamesst.append(sym['name'])
										namesOBLIG.append(sym['name'])
							else:
								if mt5.market_book_add(sym['name']):
									allnamesst.append(sym['name'])
									namesMOEX2 .append(sym['name'])

						if "MCUR\\crossrate" in sym['path'] :
							if mt5.symbol_select(sym['name'], True):
								namesCURcross.append(sym['name'])
								allnamesab.append(sym['name'])
						if "Indicative continuous\\Сырье\\" in sym['path'] :
							if mt5.symbol_select(sym['name'], True):
								namesRAW.append(sym['name'])
								allnamesab.append(sym['name'])

					print("размотали имена за", time.time() - timer)

					print(len(allnamesst)+len(allnamesab), " из них  стаканы  ",len(allnamesst), " только аск/бид ", len(allnamesab) )
					print(f' namesFRTS2   {len(namesFRTS2 )}')
					print(f' namesMOEX2  {len(namesMOEX2)} ')
					if sboroblig:
						print(f' namesOBLIG  {len(namesOBLIG)}  ')
					print(f' namesUSAFUT  {len(namesUSAFUT)}  ')
					print(f' namesCUR  {len(namesCUR)}  ')
					print(f' namesRAW   {len(namesRAW)}')
					print(f'  namesCURcross {len(namesCURcross)} ')


					count=0
					namestodel=[]
					for sym in allsym:
						sym = allsym[sym]
						if sym['select']==True:  #'visible'   'select'
							count+=1
							if sym['name'] not in allnamesst and sym['name'] not in allnamesab:
								namestodel.append(sym['name'])
								mt5.market_book_release(sym['name'])
								mt5.symbol_select(sym['name'], False)
					print( "Выбрано символов",count,"    Лишние символы в количестве",len(namestodel),"  подробней -  ", namestodel)
					if count >4900:
							print(" ВНИМАНИЕ!  ПРЕГРУЗКА по количеству символов!!!!!!!!! ")

				# тупо вгоняем стаканы в словарь -чтобы сэкономить 0,2 секунды в среднем на обработке  -чтобы меньшить рассинхрон
				slovarab = {}
				stslovar={}
				# timer =time.time()
				for name in namesFRTS2:
					stslovar[name]= mt5.market_book_get(name)
				for name in namesUSAFUT:
					stslovar[name] = mt5.market_book_get(name)
				for name in namesCUR:
					stslovar[name] = mt5.market_book_get(name)
				for name in namesRAW:
					slovarab[name] = mt5.symbol_info(name)
				for name in namesCURcross:
					slovarab[name] = mt5.symbol_info(name)
				for name in namesMOEX2:
					stslovar[name] = mt5.market_book_get(name)
				if sboroblig:
					for name in namesOBLIG:
						stslovar[name] = mt5.market_book_get(name)
				# print("получено за", time.time() - timer)

				# обработка словаря на сборщик
				# timer =time.time()
				for name in namesFRTS2:
					ab,st= getstakan (stslovar[name])
					SborFRTS2.putter(name, ab, st)
				for name in namesUSAFUT:
					ab, st = getstakan(stslovar[name])
					SborUSAFUT.putter(name, ab, st)
				for name in namesCUR:
					ab, st = getstakan(stslovar[name])
					SborCUR.putter(name, ab, st)
				for name in namesMOEX2:
					ab, st = getstakan(stslovar[name])
					SborMOEX2.putter(name, ab, st)
				if sboroblig:
					for name in namesOBLIG:
						ab, st = getstakan(stslovar[name])
						SborOBLIG.putter(name, ab, st)
				for name in namesCURcross:
					ab, st = getAB(slovarab[name])
					SborCURcross.putter(name, ab, st)
				for name in namesRAW:
					ab, st = getAB(slovarab[name])
					SborRAW.putter(name, ab, st)
				# print("обработано за" , time.time()-timer )
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------

