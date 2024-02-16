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

# mysyms = {'GD', 'SV', 'BR', 'NG', 'W4', 'Eu', 'Si', 'MX','ED','SR','SP'}
# myklaster = ['MAIN', 'NEAR', 'USAFUT', 'FAR']
myklaster = ['MAIN', 'NEAR']
mysyms = ['GD']

markets = ['MOEX2', 'FRTS2', 'CURcross', 'USAFUT', 'CUR', 'RAW', 'FxMETBR', 'FxCUR']
# markets = ['FRTS2']  # ,'MOEX'


instdict = dict()

# sym1 = 'SiM4*FRTS2'
# sym2 = 'USD000UTSTOM*CUR'

zaderzka = 3
comis = 0.03
comismaker = 0.01
minkso = comis /10


dats = {'Si': ['NGH4*FRTS2',  'NGG4*FRTS2']} #,'NGF4*FRTS2'
persrs = [500]
kpersos = [2]  # период СКО = persr *kperso
ksovhs = [1,1.5]
koefvihs = [1] # <=1

minutki = 0
onlymerge = 0
start_year, start_month, start_day, start_hour = 2024, 1, 23, 4
sstop_year, sstop_month, sstop_day, sstop_hour = 2024, 1, 30, 20

content = getdata_merge(onlymerge, minutki, markets, 'G:\\DATA_SBOR', start_year, start_month, start_day, start_hour, sstop_year,
						sstop_month, sstop_day, sstop_hour)
print(content)

traderazryv = 3
tradevozobnov = 1
exem = Getl2(content, 300, 0.95, 5)
scie = Mysredndiskret(300)

z = exem.get_l2NEW()  # получает словарь котиров
day0 = -1

# persrs = [1000,2000,4000,8000]
# kpersos = [1,2,3] # период СКО = persr *kperso
# ksovhs = [1,1.3,1.9]
# koefvihs = [1]




flagsell = dict()
flagbuy = dict()
flagsellvih = dict()
flagbuyvih = dict()

sellopenprice1 = dict()
buyopenprice2 = dict()
sellopenprice1f = dict()
buyopenprice2f = dict()
sellcloseprice1 = dict()
buycloseprice2 = dict()
sellcloseprice1f = dict()
buycloseprice2f = dict()
buycloseprice1 = dict()
sellcloseprice2 = dict()
buycloseprice1f = dict()
sellcloseprice2f = dict()
buyopenprice1 = dict()
sellopenprice2 = dict()
buyopenprice1f = dict()
sellopenprice2f = dict()

profrez1 = dict()
profrez2 = dict()
profrezall = dict()
profrez1f = dict()
profrez2f = dict()
profrezallf = dict()
profrezixes = dict()
profcomis = dict()
nakprofrez1 = dict()
nakprofrez2 = dict()
nakprofrez1f = dict()
nakprofrez2f = dict()
ksdelok = dict()
countprofrezixes = dict()

paintdictasksspread = dict()
paintdictbidsspread = dict()
paintdictixes = dict()
paintdictaskot = dict()
paintdictbidot = dict()
ct = dict()


counttotrade = dict()
totrade = dict()


eqcountprofrezixes = 0
eqprofrezixes = []

eqprofrez1 = dict()
eqprofrez2 = dict()
eqprofrezall = dict()
eqprofrez1f = dict()
eqprofrez2f = dict()
eqprofrezallf = dict()
eqprofcomis = dict()
fixprof1 = dict()
fixprof2 = dict()

EQ=dict()


sym1 = 'SiM4*FRTS2'
# sym2 = 'USD000UTSTOM*CUR'

# sym1='SiH4*FRTS2'
# sym1='SiM4*FRTS2'
# sym1='SiU4*FRTS2'
# sym2='USD000UTSTOM*CUR'
# sym2='USD000000TOD*CUR'
# sym2= 'USDRUBF*FRTS2'

REZdict=dict()
# dats = {'Si': ['SiM4*FRTS2',  'USDRUBF*FRTS2']}  # , 'SiU4*FRTS2' 'USD000UTSTOM*CUR'   'USDRUBF*FRTS2', 'SiU4*FRTS2'


onetwomas = []
countd = 0

dAsk = dict()
dBid = dict()
dAskf = dict()
dBidf = dict()
REZ=dict()
status=dict()

factsigbuy = dict()
factsigbuyvih = dict()
factsigsell = dict()
factsigsellvih = dict()

#событие -сигнал по символу -сбрасывать после проверки
event=dict()
for i in dats['Si']:
	event[i]=False
	countd += 1
	for j in dats['Si'][countd:]:
		onetwomas.append([i, j])
for onetwo, persr, kperso, ksovh, koefvih in itertools.product(onetwomas, persrs, kpersos, ksovhs, koefvihs):
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

	id = sym1 + '@' + sym2 + '@' + str(persr) + '@' + str(kperso) + '@' + str(ksovh) + '@' + str(koefvih)

	idsym1 = sym1 + '@' + sym2 + '@' + str(persr) + '@' + str(kperso) + '@' + str(ksovh) + '@' + str(koefvih)
	idsym2 = sym2 + '@' + sym1 + '@' + str(persr) + '@' + str(kperso) + '@' + str(ksovh) + '@' + str(koefvih)

	# сигнал  есль или нет
	factsigbuy[idsym1]=False
	factsigbuyvih [idsym1]=False
	factsigsell[idsym1]=False
	factsigsellvih[idsym1]=False
	factsigbuy[idsym1]=False
	factsigbuyvih [idsym1]=False
	factsigsell[idsym1]=False
	factsigsellvih[idsym1]=False

	factsigbuy[idsym2]=False
	factsigbuyvih [idsym2]=False
	factsigsell[idsym2]=False
	factsigsellvih[idsym2]=False
	factsigbuy[idsym2]=False
	factsigbuyvih [idsym2]=False
	factsigsell[idsym2]=False
	factsigsellvih[idsym2]=False


	ids= sym1 + '@' + sym2
	id2 = sym1 + '@' + sym2 + '@' + str(persr)
	print(id)

	status[ids] = False

	counttotrade[id2] = 0
	totrade[id2] = True

	flagsell[id] = True
	flagbuy[id] = True
	flagsellvih[id] = False
	flagbuyvih[id] = False

	sellopenprice1[id] = None
	buyopenprice2[id] = None
	sellopenprice1f[id] = None
	buyopenprice2f[id] = None
	sellcloseprice1[id] = None
	buycloseprice2[id] = None
	sellcloseprice1f[id] = None
	buycloseprice2f[id] = None
	buycloseprice1[id] = None
	sellcloseprice2[id] = None
	buycloseprice1f[id] = None
	sellcloseprice2f[id] = None
	buyopenprice1[id] = None
	sellopenprice2[id] = None
	buyopenprice1f[id] = None
	sellopenprice2f[id] = None

	profrez1[id] = []
	profrez2[id] = []
	profrezall[id] = []
	profrez1f[id] = []
	profrez2f[id] = []
	profrezallf[id] = []
	profrezixes[id] = []
	profcomis[id] = []
	nakprofrez1[id] = 0
	nakprofrez2[id] = 0
	nakprofrez1f[id] = 0
	nakprofrez2f[id] = 0
	ksdelok[id] = 0
	countprofrezixes[id] = -1

	paintdictasksspread[id] = []
	paintdictbidsspread[id] = []
	paintdictixes[id] = []
	paintdictaskot[id] = []
	paintdictbidot[id] = []
	ct[id] = -1

	eqprofrez1[id] = []
	eqprofrez2[id] = []
	eqprofrezall[id] = []
	eqprofrez1f[id] = []
	eqprofrez2f[id] = []
	eqprofrezallf[id] = []
	eqprofcomis[id] = []
	EQ[id] = []
	REZ[id]  = []
	fixprof1[id]  = []
	fixprof2[id]  = []





zadr = deque()
for i in range(zaderzka):
	data0 = next(z).copy()
	zadr.append(data0)

timer = time.time()
hour0 = -1
# counthour=0
Ask1 =None
Bid1 = None
Ask2 = None
Bid2 = None
Ask1f =None
Bid1f = None
Ask2f = None
Bid2f = None





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
		for onetwo in onetwomas:
			sym1 = onetwo[0]
			sym2 = onetwo[1]
			ids = sym1 + '@' + sym2

			status[ids] = False
			if sym1 in data and sym2 in data:
				if data[sym1]['dat'] != None and data[sym2]['dat'] != None:
					if data[sym1]['tmstp'][2] and data[sym2]['tmstp'][2]:
						status[ids]=True


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
											for koefvih in koefvihs:
												id = sym1 + '@' + sym2 + '@' + str(persr) + '@' + str(kperso) + '@' + str(ksovh) + '@' + str(koefvih)

												idsym1 = sym1 + '@' + sym2 + '@' + str(persr) + '@' + str(kperso) + '@' + str(ksovh) + '@' + str(koefvih)
												idsym2 = sym2 + '@' + sym1 + '@' + str(persr) + '@' + str(kperso) + '@' + str(ksovh) + '@' + str(koefvih)

												# ************************************************
												ct[id] += 1
												paintdictixes[id].append(ct[id])
												paintdictasksspread[id].append(Asksp)
												paintdictbidsspread[id].append(Bidsp)
												paintdictaskot[id].append(SoAsk * ksovh)
												paintdictbidot[id].append(SoBid * ksovh)

												ksovih = ksovh * koefvih

												# ************************************************
												# ************************************************

												# закрытие продажи  покупкой
												if Asksp < SoBid * ksovih  and totrade[id0]:  # Asksp<SoBid
													factsigbuyvih[idsym2] = True
													factsigsellvih[idsym1] = True
													if flagsellvih[id]:
														REZ[id].append(['sellvih', [Ask1, Bid1], [Ask2, Bid2], [Ask1f, Bid1f], [Ask2f, Bid2f]])
														event[sym1]=True
														event[sym2] = True
														flagsellvih[id] = False
														flagsell[id] = True
														flagbuy[id] = True

														nakprofrez1[id] += 100 * (sellopenprice1[id] - Ask1) / sellopenprice1[id]
														nakprofrez2[id] += 100 * (Bid2 - buyopenprice2[id]) / buyopenprice2[id]
														nakprofrez1f[id] += 100 * (sellopenprice1f[id] - Ask1f) / sellopenprice1f[id]
														nakprofrez2f[id] += 100 *(Bid2f- buyopenprice2f[id]) / buyopenprice2f[id]


														profrez1[id].append(nakprofrez1[id])
														profrez2[id].append(nakprofrez2[id])
														profrez1f[id].append(nakprofrez1f[id])
														profrez2f[id].append(nakprofrez2f[id])
														profrezallf[id].append(nakprofrez1f[id] + nakprofrez2f[id])
														profrezall[id].append(nakprofrez1[id] + nakprofrez2[id])

														countprofrezixes[id] += 1
														profrezixes[id].append(countprofrezixes[id])
														ksdelok[id] += 1
														profcomis[id].append(ksdelok[id] * comis)


												# закрытие покупки продажей
												if Bidsp > SoAsk * ksovih  and totrade[id0]:  # Bidsp>SoAsk
													factsigbuyvih[idsym1] = True
													factsigsellvih[idsym2] = True
													if flagbuyvih[id]:
														REZ[id].append(['buyvih', [Ask1, Bid1], [Ask2, Bid2], [Ask1f, Bid1f], [Ask2f, Bid2f]])

														event[sym1] = True
														event[sym2] = True
														flagbuyvih[id] = False
														flagbuy[id] = True
														flagsell[id] = True


														nakprofrez1[id] +=100 * (Bid1 - buyopenprice1[id]) / buyopenprice1[id]
														nakprofrez2[id] += 100 * (sellopenprice2[id] - Ask2) / sellopenprice2[id]
														nakprofrez1f[id] += 100 * (Bid1f - buyopenprice1f[id]) / buyopenprice1f[id]
														nakprofrez2f[id] += 100 * (sellopenprice2f[id] - Ask2f) / sellopenprice2f[id]

														profrez1[id].append(nakprofrez1[id])
														profrez2[id].append(nakprofrez2[id])


														profrez1f[id].append(nakprofrez1f[id])
														profrez2f[id].append(nakprofrez2f[id])

														profrezallf[id].append(nakprofrez1f[id] + nakprofrez2f[id])
														profrezall[id].append(nakprofrez1[id] + nakprofrez2[id])

														countprofrezixes[id] += 1
														profrezixes[id].append(countprofrezixes[id])
														ksdelok[id] += 1
														profcomis[id].append(ksdelok[id] * comis)
											# ************************************************

												# продажа
												if Bidsp > SoAsk * ksovh  and So > minkso and totrade[id0]:  # and (So1-So2) >So/2:
													factsigbuy[idsym2] =True
													factsigsell[idsym1] =True
													if flagsell[id]:
														REZ[id].append(['sell', [Ask1, Bid1], [Ask2, Bid2], [Ask1f, Bid1f], [Ask2f, Bid2f]])
														event[sym1] = True
														event[sym2] = True
														flagsell[id] = False
														flagbuy[id] = False
														flagsellvih[id] = True
														sellopenprice1[id] = Bid1
														buyopenprice2[id] = Ask2
														sellopenprice1f[id] = Bid1f
														buyopenprice2f[id] = Ask2f
												# покупка
												if Asksp < SoBid * ksovh  and So > minkso and totrade[id0]:  # and (So1-So2) >So/2:
													factsigbuy[idsym1] = True
													factsigsell[idsym2] = True
													if flagbuy[id]:
														REZ[id].append(['buy', [Ask1, Bid1], [Ask2, Bid2], [Ask1f, Bid1f], [Ask2f, Bid2f]])
														event[sym1] = True
														event[sym2] = True
														flagbuy[id] = False
														flagsell[id] = False
														flagbuyvih[id] = True
														buyopenprice1[id] = Ask1
														sellopenprice2[id] = Bid2
														buyopenprice1f[id] = Ask1f
														sellopenprice2f[id] = Bid2f

		#
		# фиксация эквити раз в час  закрытие покупки продажей
		if hour0 != hour:
			hour0 = hour

			# counthour+=1
			eqcountprofrezixes += 1
			eqprofrezixes.append(eqcountprofrezixes)
			onetwomas = []
			countd = 0
			for i in dats['Si']:
				countd += 1
				for j in dats['Si'][countd:]:
					onetwomas.append([i, j])
			for onetwo, persr, kperso, ksovh, koefvih in itertools.product(onetwomas, persrs, kpersos, ksovhs, koefvihs):
				sym1 = onetwo[0]
				sym2 = onetwo[1]
				ids = sym1 + '@' + sym2
				id = sym1 + '@' + sym2 + '@' + str(persr) + '@' + str(kperso) + '@' + str(ksovh) + '@' + str(koefvih)

				EQ[id].append([tme, [[dAsk[sym1], dBid[sym1]], [dAsk[sym2], dBid[sym2]], [dAskf[sym1], dBidf[sym1]], [dAskf[sym2], dBidf[sym2]]], REZ[id], status[ids]])
				REZ[id] = []

				if not flagbuyvih[id] and not flagsellvih[id]:
					Reqprofrez1 = (nakprofrez1[id])
					Reqprofrez2 = (nakprofrez2[id])

					Reqprofrez1f = (nakprofrez1f[id])
					Reqprofrez2f = (nakprofrez2f[id])

				if flagsellvih[id]:
					Reqprofrez1 = (nakprofrez1[id] + 100 * (sellopenprice1[id] - dAsk[sym1]) / sellopenprice1[id])
					Reqprofrez2 = (nakprofrez2[id] + 100 * (dBid[sym2] - buyopenprice2[id]) / buyopenprice2[id])

					Reqprofrez1f = (nakprofrez1f[id] + 100 * (sellopenprice1f[id] - dAskf[sym1]) / sellopenprice1f[id])
					Reqprofrez2f = (nakprofrez2f[id] + 100 * (dBidf[sym2] - buyopenprice2f[id]) / buyopenprice2f[id])

				if flagbuyvih[id]:
					Reqprofrez1 = (nakprofrez1[id] + 100 * (dBid[sym1] - buyopenprice1[id]) / buyopenprice1[id])
					Reqprofrez2 = (nakprofrez2[id] + 100 * (sellopenprice2[id] - dAsk[sym2]) / sellopenprice2[id])

					Reqprofrez1f = (nakprofrez1f[id] + 100 * (dBidf[sym1] - buyopenprice1f[id]) / buyopenprice1f[id])
					Reqprofrez2f = (nakprofrez2f[id] + 100 * (sellopenprice2f[id] - dAskf[sym2]) / sellopenprice2f[id])

				#  добавим
				eqprofrez1[id].append(Reqprofrez1)
				eqprofrez2[id].append(Reqprofrez2)

				eqprofrez1f[id].append(Reqprofrez1f)
				eqprofrez2f[id].append(Reqprofrez2f)

				eqprofrezall[id].append(Reqprofrez1 + Reqprofrez2)
				eqprofrezallf[id].append(Reqprofrez1f + Reqprofrez2f)

				eqprofcomis[id].append(ksdelok[id] * comis)

				fixprof1[id].append(nakprofrez1[id])
				fixprof2[id].append(nakprofrez2[id])






	# except:
	except Exception:
		print(traceback.format_exc())
		print('error')
		break

myput('rez6',EQ)
# print('PAINT', sym1, "  ", sym2,'   ',persrs)
print(f'time = {time.time() - timer}')
# for persr,kperso,ksovh,koefvih in itertools.product(persrs, kpersos,ksovhs,koefvihs ):
for onetwo, persr, kperso, ksovh, koefvih in itertools.product(onetwomas, persrs, kpersos, ksovhs, koefvihs):
	sym1 = onetwo[0]
	sym2 = onetwo[1]
	id = sym1 + '@' + sym2 + '@' + str(persr) + '@' + str(kperso) + '@' + str(ksovh) + '@' + str(koefvih)
	color = get_color()
	fig = px.line( title=f"D id {id}  ")
	clr = color()
	fig.add_scatter(x=profrezixes[id], y=profrez1[id], line_color=clr, name=sym1 + " - " + ' profrez1')
	clr = color()
	fig.add_scatter(x=profrezixes[id], y=profrez2[id], line_color=clr, name=sym2 + " - " + ' profrez2')
	clr = color()
	fig.add_scatter(x=profrezixes[id], y=profrezall[id], line_color=clr, name=' profrezall')
	clr = color()
	fig.add_scatter(x=profrezixes[id], y=profrez1f[id], line_color=clr, name=sym1 + " - " + ' profrez1f')
	clr = color()
	fig.add_scatter(x=profrezixes[id], y=profrez2f[id], line_color=clr, name=sym2 + " - " + ' profrez2f')
	clr = color()
	fig.add_scatter(x=profrezixes[id], y=profrezallf[id], line_color=clr, name=' profrezallf')

	clr = color()
	fig.add_scatter(x=profrezixes[id], y=profcomis[id], line_color=clr, name='comis')
	fig.show()


	color = get_color()
	fig = px.line( title=f"D REZ eq {id} ")
	clr = color()
	fig.add_scatter(x=eqprofrezixes, y=eqprofrez1[id], line_color=clr, name=sym1 + " - " + ' eqprofrez1')
	clr = color()
	fig.add_scatter(x=eqprofrezixes, y=eqprofrez2[id], line_color=clr, name=sym2 + " - " + ' eqprofrez2')
	clr = color()
	fig.add_scatter(x=eqprofrezixes, y=eqprofrez1f[id], line_color=clr, name=sym1 + " - " + ' eqprofrez1f')
	clr = color()
	fig.add_scatter(x=eqprofrezixes, y=eqprofrez2f[id], line_color=clr, name=sym2 + " - " + ' eqprofrez2f')
	clr = color()
	fig.add_scatter(x=eqprofrezixes, y=eqprofrezall[id], line_color=clr, name=' eqprofrezall')
	clr = color()
	fig.add_scatter(x=eqprofrezixes, y=eqprofrezallf[id], line_color=clr, name=' eqprofrezallf')

	clr = color()
	fig.add_scatter(x=eqprofrezixes, y=fixprof1[id], line_color=clr, name=' fixprof1')
	clr = color()
	fig.add_scatter(x=eqprofrezixes, y=fixprof2[id], line_color=clr, name=' fixprof2')

	clr = color()
	fig.add_scatter(x=eqprofrezixes, y=eqprofcomis[id], line_color=clr, name='eqcomis')
	fig.show()

	color = get_color()
	fig = px.line( 	title=f"D id {id}  ")
	clr = color()
	fig.add_scatter(x=paintdictixes[id], y=paintdictasksspread[id], line_color=clr, name= ' askSpread')
	fig.add_scatter(x=paintdictixes[id], y=paintdictbidsspread[id], line_color=clr, name=' bidSpread')
	clr = color()
	fig.add_scatter(x=paintdictixes[id], y=paintdictaskot[id] ,line_color=clr, name=' askot')
	fig.add_scatter(x=paintdictixes[id], y=paintdictbidot[id], line_color=clr, name=' bidot')
	fig.show()