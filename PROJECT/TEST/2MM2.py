from PROJECT.TEST.Test_lib import *
from PROJECT.VIZUAL.Viz_lib import get_color
from PROJECT.SCIENTIC.sc_sredn_lib import *
from platform import system
import plotly.express as px
from collections import deque
import datetime, time  # timer=time.time()
import traceback
from statistics import mean
from PROJECT.SBOR.my_lib import *
from get_my_insts import get_fut
import itertools
import copy

# mysyms = {'GD', 'SV', 'BR', 'NG', 'W4', 'Eu', name, 'MX','ED','SR','SP'}
# myklaster = ['MAIN', 'NEAR', 'USAFUT', 'FAR']
myklaster = ['MAIN', 'NEAR']
# mysyms = ['GD']

# markets = ['MOEX2', 'FRTS2', 'CURcross', 'USAFUT', 'CUR', 'RAW', 'FxMETBR', 'FxCUR']
markets = ['FRTS2',  'MOEX2']  # ,'MOEX'


instdict = dict()

# sym1 = 'SiM4*FRTS2'
# sym2 = 'USD000UTSTOM*CUR'


# Январь – F
# Февраль – G
# Март – H
# Апрель – J
# Май – K
# Июнь – M
# Июль – N
# Август – Q
# Сентябрь – U
# Октябрь – V
# Ноябрь – X
# Декабрь – Z

zaderzka = 3
comis = 0.01
comismaker = 0.01
minkso = comis

name='SP'
dats = {name: ['SPH4*FRTS2', 'SPM4*FRTS2', 'SBERP*MOEX2','SRH4*FRTS2', 'SRM4*FRTS2', 'SRU4*FRTS2', 'SRZ4*FRTS2', 'SBER*MOEX2']}  # ,'NGF4*FRTS2'

persrs = [100,500,5000,10000]
kpersos = [2]  # период СКО = persr *kperso
ksovhs = [0,1,1.5,2]


minutki = 0
onlymerge = 0
start_year, start_month, start_day, start_hour = 2024, 1, 17, 4
sstop_year, sstop_month, sstop_day, sstop_hour = 2024, 2, 17, 20

content = getdata_merge(onlymerge, minutki, markets, 'G:\\DATA_SBOR', start_year, start_month, start_day, start_hour, sstop_year,
						sstop_month, sstop_day, sstop_hour)
print(content)

traderazryv = 3
tradevozobnov = 1
exem = Getl2(content, 300, 0.95, 5)
scie = Mysredndiskret(300)

z = exem.get_l2NEW()  # получает словарь котиров
day0 = -1

flagsell = dict()
flagbuy = dict()
flagsellvih = dict()
flagbuyvih = dict()

counttotrade = dict()
totrade = dict()




onetwomas = []
countd = 0
dAsk = dict()
dBid = dict()
dAskf = dict()
dBidf = dict()
REZ = dict()
status = dict()

for i in dats[name]:

	countd += 1
	for j in dats[name][countd:]:
		onetwomas.append([i, j])
for onetwo, persr, kperso, ksovh in itertools.product(onetwomas, persrs, kpersos, ksovhs):
	sym1 = onetwo[0]
	sym2 = onetwo[1]
	dAsk[sym1] = None
	dBid[sym1] = None
	dAskf[sym1] = None
	dBidf[sym1] = None
	dAsk[sym2] = None
	dBid[sym2] = None
	dAskf[sym2] = None
	dBidf[sym2] = None

	id = sym1 + '@' + sym2 + '@' + str(persr) + '@' + str(kperso) + '@' + str(ksovh)
	ids = sym1 + '@' + sym2
	id2 = sym1 + '@' + sym2 + '@' + str(persr)
	print(id)

	status[ids] = False

	counttotrade[id2] = 0
	totrade[id2] = True

	flagsell[id] = True
	flagbuy[id] = True
	flagsellvih[id] = False
	flagbuyvih[id] = False



zadr = deque()
for i in range(zaderzka):
	data0 = next(z).copy()
	zadr.append(data0)

timer = time.time()
hour0 = -1
# counthour=0
Ask1 = None
Bid1 = None
Ask2 = None
Bid2 = None
Ask1f = None
Bid1f = None
Ask2f = None
Bid2f = None
tme = None
bigstruct = dict()
# bigstruct['time']=dict()
mystruct = dict()
for persr in persrs:
	for kperso in kpersos:
		for ksovh in ksovhs:
			idev = str(persr) + '@' + str(kperso) + '@' + str(ksovh)
			mystruct[idev] = dict()
			for sym in dats[name]:
				mystruct[idev][sym] = []
idevmas=[]
lastsignals = dict()
for persr in persrs:
	for kperso in kpersos:
		for ksovh in ksovhs:
			idev = str(persr) + '@' + str(kperso) + '@' + str(ksovh)
			idevmas.append(idev)
			lastsignals[idev] = dict()
			for sym in dats[name]:
				lastsignals[idev][sym] = dict()
				lastsignals[idev][sym]['buy'] = set()
				lastsignals[idev][sym]['sell'] = set()
# master=dict()
while True:
	try:
		# print(f'time = {time.time() - timer}')
		# timer = time.time()
		futuredata = next(z).copy()  # это якобы на серваке - к нему нужен доступ
		zadr.append(futuredata)
		data = zadr.popleft()

		tme = exem.ttime  # Эмуляция получения времени
		day = exem.day
		hour = exem.hr
		#  эмуляция получения списка инструментов  раз в день
		if day != day0:
			day0 = day
			year = exem.year
			month = exem.mon

		#  TUT NADO VOYAT
		# лень менять прошлую структуру - раскидаю сигралы после каждой секунды, хоть это и не так эффективно
		# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

		signals = dict()
		for idev in idevmas:
			signals[idev] = dict()
			for sym in dats[name]:
				signals[idev][sym] = dict()
				signals[idev][sym]['buy'] = set()
				signals[idev][sym]['sell'] = set()



		for onetwo in onetwomas:
			sym1 = onetwo[0]
			sym2 = onetwo[1]
			ids = sym1 + '@' + sym2

			status[ids] = False
			if sym1 in data and sym2 in data:
				if data[sym1]['dat'] != None and data[sym2]['dat'] != None:
					if data[sym1]['tmstp'][2] and data[sym2]['tmstp'][2]:
						status[ids] = True

						Ask1 = data[sym1]['dat'][0]
						Bid1 = data[sym1]['dat'][1]
						Ask2 = data[sym2]['dat'][0]
						Bid2 = data[sym2]['dat'][1]

						Ask1f = futuredata[sym1]['dat'][0]
						Bid1f = futuredata[sym1]['dat'][1]
						Ask2f = futuredata[sym2]['dat'][0]
						Bid2f = futuredata[sym2]['dat'][1]

						dAsk[sym1] = Ask1
						dBid[sym1] = Bid1
						dAsk[sym2] = Ask2
						dBid[sym2] = Bid2

						dAskf[sym1] = Ask1f
						dBidf[sym1] = Bid1f
						dAskf[sym2] = Ask2f
						dBidf[sym2] = Bid2f

						# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
						for persr in persrs:
							id0 = sym1 + '@' + sym2 + '@' + str(persr)
							# обзначим разрывы больше средней* tradevozobnov
							# ****************************************
							if totrade[id0] and (data[sym1]['tmstp'][1] > persr * traderazryv or data[sym2]['tmstp'][1] > persr * traderazryv):
								print(' RAZRIV ', day, ' ', exem.hr)
								counttotrade[id0] = 0
								totrade[id0] = False
							counttotrade[id0] += 1
							if totrade[id0] == False and counttotrade[id0] > persr * tradevozobnov:
								totrade[id0] = True
							# ****************************************

							sredn1 = scie.getshlifmed_easy((Ask1 + Bid1) / 2, '1' + id0, persr)
							sredn2 = scie.getshlifmed_easy((Ask2 + Bid2) / 2, '2' + id0, persr)
							if sredn1 != None and sredn2 != None:
								Asksp = 100 * Ask1 / sredn1 - 100 * Bid2 / sredn2
								Bidsp = 100 * Bid1 / sredn1 - 100 * Ask2 / sredn2
								# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
								for kperso in kpersos:
									id = sym1 + '@' + sym2 + '@' + str(persr) + '@' + str(kperso)
									So = scie.getshlifmed_easy(max(abs(Asksp), abs(Bidsp)), 'So' + id, persr * kperso)
									if So != None:
										# ************************************************
										SoAsk = So
										SoBid = 0 - So
										# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
										for ksovh in ksovhs:
											# ************************************************
											# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

											idev = str(persr) + '@' + str(kperso) + '@' + str(ksovh)

											# продажа
											if Bidsp > max(SoAsk * ksovh,minkso) and totrade[id0]:  # and (So1-So2) >So/2:
												signals[idev][sym1]['sell'].add(sym2)
												signals[idev][sym2]['buy'].add(sym1)

											# покупка
											if Asksp < min(SoBid * ksovh,-minkso) and totrade[id0]:  # and (So1-So2) >So/2:
												signals[idev][sym1]['buy'].add(sym2)
												signals[idev][sym2]['sell'].add(sym1)



		# лучше бы переделать по словарям изначально, но попарсим.
		# случилось событие -вписываем все сигналы  чоглвчно стрyктурe
		for idev in idevmas:
			for sym in dats[name]:

				if signals[idev][sym]['buy'] != lastsignals[idev][sym]['buy'] and signals[idev][sym]['sell'] != lastsignals[idev][sym]['sell']:
					lastsignals[idev][sym]['buy'] = copy.deepcopy(signals[idev][sym]['buy'])
					lastsignals[idev][sym]['sell'] = copy.deepcopy(signals[idev][sym]['sell'])
					mystruct[idev][sym].append([dAsk[sym], dBid[sym], dAskf[sym], dBidf[sym], {'buy': list(signals[idev][sym]['buy']),'sell':list(signals[idev][sym]['sell'])}])
				else:
					if signals[idev][sym]['buy'] !=lastsignals[idev][sym]['buy']:
						lastsignals[idev][sym]['buy']= copy.deepcopy(signals[idev][sym]['buy'])
						mystruct[idev][sym].append([dAsk[sym], dBid[sym], dAskf[sym], dBidf[sym],{'buy': list(signals[idev][sym]['buy']) }])

					elif signals[idev][sym]['sell'] != lastsignals[idev][sym]['sell']:
						lastsignals[idev][sym]['sell'] = copy.deepcopy(signals[idev][sym]['sell'])
						mystruct[idev][sym].append([dAsk[sym], dBid[sym], dAskf[sym], dBidf[sym], {'sell':list(signals[idev][sym]['sell'])} ])



		# фиксация эквити раз в час  закрытие покупки продажей
		if hour0 != hour:
			hour0 = hour
			stime = str(tme)
			bigstruct[stime] = dict()
			bigstruct[stime]['asks'] = copy.deepcopy(dAsk)
			bigstruct[stime]['bids'] = copy.deepcopy(dBid)
			bigstruct[stime]['data'] = copy.deepcopy(mystruct)

			mystruct = dict()
			for persr in persrs:
				for kperso in kpersos:
					for ksovh in ksovhs:
						idev = str(persr) + '@' + str(kperso) + '@' + str(ksovh)
						mystruct[idev] = dict()
						for sym in dats[name]:
							mystruct[idev][sym] = []



	# except:
	except Exception:
		print(traceback.format_exc())
		print('error')
		break

if tme != None:
	stime = str(tme)
	bigstruct[stime] = dict()
	bigstruct[stime]['asks'] = copy.deepcopy(dAsk)
	bigstruct[stime]['bids'] = copy.deepcopy(dBid)
	bigstruct[stime]['data'] = copy.deepcopy(mystruct)
	# dAsk
	mystruct = dict()
	for persr in persrs:
		for kperso in kpersos:
			for ksovh in ksovhs:
				idev = str(persr) + '@' + str(kperso) + '@' + str(ksovh)
				mystruct[idev] = dict()
				for sym in dats[name]:
					mystruct[idev][sym] = []


myput(name+'bigstruct', bigstruct)
print(f'time = {time.time() - timer}')
