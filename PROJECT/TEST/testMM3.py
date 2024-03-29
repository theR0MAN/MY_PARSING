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
comismaker=0.01
# persr = 2000  # период средней
# kperso = 3  # период СКО = persr *kperso
# ksovh = 1
# koefvih=1
minkso = comis

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




mytradesellimit =dict() 
mytradebuylimit =dict()
mytradepositionbuy =dict() 
mytradepositionsell =dict() 
mytraderezults =dict()
naklimrez =dict() 

mytradesellimit2 =dict() 
mytradebuylimit2 =dict() 
mytradepositionbuy2 =dict() 
mytradepositionsell2 =dict()
mytraderezults2 =dict() 
naklimrez2 =dict() 

flagsell =dict() 
flagbuy =dict() 
flagsellvih =dict() 
flagbuyvih =dict() 

sellopenprice1 =dict() 
buyopenprice2 =dict() 
sellopenprice1f =dict() 
buyopenprice2f =dict() 
sellcloseprice1 =dict() 
buycloseprice2 =dict() 
sellcloseprice1f =dict()
buycloseprice2f =dict()
buycloseprice1=dict()
sellcloseprice2=dict()
buycloseprice1f=dict()
sellcloseprice2f=dict()
buyopenprice1=dict()
sellopenprice2=dict()
buyopenprice1f=dict()
sellopenprice2f=dict()


profrez1 =dict() 
profrez2 =dict() 
profrezall =dict() 
profrez1f =dict() 
profrez2f =dict() 
profrezallf =dict() 
profrezixes =dict() 
profcomis =dict() 
nakprofrez1 =dict() 
nakprofrez2 =dict() 
nakprofrez1f =dict() 
nakprofrez2f =dict() 
ksdelok =dict() 
countprofrezixes =dict()


paintdictasksspread = dict()
paintdictbidsspread = dict()
paintdictixes = dict()
paintdictaskot = dict()
paintdictbidot = dict()
ct=dict()



volamaxsell1 = dict()
volaminsell1 = dict()
volamaxbuy1  =dict()
volaminbuy1 =  dict()
masotnvola1=dict()
nakotnvola1=dict()

volamaxsell2 = dict()
volaminsell2 = dict()
volamaxbuy2  =dict()
volaminbuy2 = dict()
masotnvola2=dict()
nakotnvola2=dict()
counttotrade =dict()
totrade =dict()


ksdeloklim1 = dict()
ksdeloklim2 = dict()
eqcountprofrezixes = 0
eqprofrezixes=[]

eqprofrez1 = dict()
eqprofrez2 = dict()
eqprofrezall =dict()
eqprofrez1f =dict()
eqprofrez2f = dict()
eqprofrezallf = dict()
eqprofcomis = dict()
eqprofcomislim1 = dict()
eqprofcomislim2 = dict()
eqmytraderezults = dict()
eqmytraderezults2 = dict()

sym1 = 'SiM4*FRTS2'
# sym2 = 'USD000UTSTOM*CUR'

# sym1='SiH4*FRTS2'
# sym1='SiM4*FRTS2'
# sym1='SiU4*FRTS2'
# sym2='USD000UTSTOM*CUR'
# sym2='USD000000TOD*CUR'
# sym2= 'USDRUBF*FRTS2'

dats = {'Si': ['SiM4*FRTS2', 'USDRUBF*FRTS2']} #, 'SiU4*FRTS2'
persrs = [1000]
kpersos = [2] # период СКО = persr *kperso
ksovhs = [1.5]
koefvihs = [1]



onetwomas=[]
countd=0
for i in dats['Si']:
	countd+=1
	for j in dats['Si'][countd:]:
		onetwomas.append([i,j])
for onetwo,persr,kperso,ksovh,koefvih in itertools.product(onetwomas,persrs, kpersos,ksovhs,koefvihs ):
	sym1 = onetwo[0]
	sym2 = onetwo[1]
	id = sym1 + '@' + sym2 + '@' + str(persr) + '@' + str(kperso) + '@' + str(ksovh) + '@' + str(koefvih)
	id2 = sym1 + '@' + sym2 + '@' + str(persr)
	print(id)



	mytradesellimit [id] =  None
	mytradebuylimit [id] =  None
	mytradepositionbuy [id] =  None
	mytradepositionsell [id] =  None
	mytraderezults [id] =  []
	naklimrez [id] =  0

	mytradesellimit2 [id] =  None
	mytradebuylimit2 [id] =  None
	mytradepositionbuy2 [id] =  None
	mytradepositionsell2 [id] =  None
	mytraderezults2 [id] =  []
	naklimrez2 [id] =  0

	flagsell [id] =  True
	flagbuy [id] =  True
	flagsellvih [id] =  False
	flagbuyvih [id] =  False

	sellopenprice1 [id] =  None
	buyopenprice2 [id] =  None
	sellopenprice1f [id] =  None
	buyopenprice2f [id] =  None
	sellcloseprice1 [id] =  None
	buycloseprice2 [id] =  None
	sellcloseprice1f [id] =  None
	buycloseprice2f [id] =  None
	buycloseprice1[id] = None
	sellcloseprice2[id] = None
	buycloseprice1f[id] = None
	sellcloseprice2f[id] = None
	buyopenprice1[id] = None
	sellopenprice2[id] = None
	buyopenprice1f[id] = None
	sellopenprice2f[id] = None

	profrez1 [id] =  []
	profrez2 [id] =  []
	profrezall [id] =  []
	profrez1f [id] =  []
	profrez2f [id] =  []
	profrezallf [id] =  []
	profrezixes [id] =  []
	profcomis [id] =  []
	nakprofrez1 [id] =  0
	nakprofrez2 [id] =  0
	nakprofrez1f [id] =  0
	nakprofrez2f [id] =  0
	ksdelok [id] =  0
	countprofrezixes [id] =  -1

	paintdictasksspread [id] =  []
	paintdictbidsspread [id] =  []
	paintdictixes [id] =  []
	paintdictaskot [id] =  []
	paintdictbidot [id] =  []
	ct[id] =  -1

	volamaxsell1[id] = -100
	volaminsell1[id] = 1000000000
	volamaxbuy1[id]  =-100
	volaminbuy1[id] =  1000000000
	masotnvola1[id]=[]
	nakotnvola1[id]=0

	volamaxsell2[id] = -100
	volaminsell2[id] = 1000000000
	volamaxbuy2[id]  =-100
	volaminbuy2[id] =  1000000000
	masotnvola2[id]=[]
	nakotnvola2[id]=0



	counttotrade[id2] = 0
	totrade[id2] = True

	ksdeloklim1[id] = 0
	ksdeloklim2[id] = 0

	eqprofrez1[id] = []
	eqprofrez2[id] = []
	eqprofrezall[id] = []
	eqprofrez1f[id] = []
	eqprofrez2f[id] = []
	eqprofrezallf[id] = []
	eqprofcomis[id] = []
	eqprofcomislim1[id] = []
	eqprofcomislim2[id] = []
	eqmytraderezults[id] = []
	eqmytraderezults2[id] = []

dAsk = dict()
dBid = dict()
dAskf = dict()
dBidf = dict()


zadr = deque()
for i in range(zaderzka):
	data0 = next(z).copy()
	zadr.append(data0)
timer = time.time()
hour0 = -1
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

		if hour0 != hour:
			hour0 = hour
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
				id = sym1 + '@' + sym2 + '@' + str(persr) + '@' + str(kperso) + '@' + str(ksovh) + '@' + str(koefvih)

				# Ask1 = dAsk[sym1]
				# Bid1 = dBid[sym1]
				# Ask2 = dAsk[sym2]
				# Bid2 = dBid[sym2]
				# Ask1f = dAskf[sym1]
				# Bid1f = dBidf[sym1]
				# Ask2f = dAskf[sym2]
				# Bid2f = dBidf[sym2]

				# цикл по айди должен быть
				if not flagbuyvih[id] and not flagsellvih[id]:
					eqprofrez1[id].append(nakprofrez1[id])
					eqprofrez2[id].append(nakprofrez2[id])

					eqprofrez1f[id].append(nakprofrez1f[id])
					eqprofrez2f[id].append(nakprofrez2f[id])

					eqprofrezall[id].append(nakprofrez1[id] + nakprofrez2[id])
					eqprofrezallf[id].append(nakprofrez1f[id] + nakprofrez2f[id])
					eqprofcomis[id].append(ksdelok[id] * comis)

				if flagsellvih[id]:

					profit1 = 100 * (sellopenprice1[id] - dAsk[sym1]) / sellopenprice1[id]
					profit2 = 100 * (dBid[sym2] - buyopenprice2[id]) / buyopenprice2[id]
					profit1f = 100 * (sellopenprice1f[id] - dAskf[sym1]) / sellopenprice1f[id]
					profit2f = 100 * (dBidf[sym2] - buyopenprice2f[id]) / buyopenprice2f[id]

					eqprofrez1[id].append(nakprofrez1[id] + profit1)
					eqprofrez2[id].append(nakprofrez2[id] + profit2)

					eqprofrez1f[id].append(nakprofrez1f[id] + profit1f)
					eqprofrez2f[id].append(nakprofrez2f[id] + profit2f)

					eqprofrezall[id].append(nakprofrez1[id] + profit1 + nakprofrez2[id] + profit2)
					eqprofrezallf[id].append(nakprofrez1f[id] + profit1f + nakprofrez2f[id] + profit2f)

					eqprofcomis[id].append(ksdelok[id] * comis)
				# фиксация эквити раз в час  закрытие покупки продажей
				if flagbuyvih[id]:

					profit1 = 100 * (dBid[sym1]- buyopenprice1[id]) / buyopenprice1[id]
					profit2 = 100 * (sellopenprice2[id] - dAsk[sym2]) / sellopenprice2[id]
					profit1f = 100 * (dBidf[sym1] - buyopenprice1f[id]) / buyopenprice1f[id]
					profit2f = 100 * (sellopenprice2f[id] - dAskf[sym2]) / sellopenprice2f[id]

					eqprofrez1[id].append(nakprofrez1[id] + profit1)
					eqprofrez2[id].append(nakprofrez2[id] + profit2)

					eqprofrez1f[id].append(nakprofrez1f[id] + profit1f)
					eqprofrez2f[id].append(nakprofrez2f[id] + profit2f)

					eqprofrezall[id].append(nakprofrez1[id] + profit1 + nakprofrez2[id] + profit2)
					eqprofrezallf[id].append(nakprofrez1f[id] + profit1f + nakprofrez2f[id] + profit2f)

					eqprofcomis[id].append(ksdelok[id] * comis)

				# limits
				if mytradepositionbuy[id] == None and mytradepositionsell[id] == None:
					eqmytraderezults[id].append(naklimrez[id])
					eqprofcomislim1[id].append(ksdeloklim1[id] * comismaker)

				if mytradepositionbuy2[id] == None and mytradepositionsell2[id] == None:
					eqmytraderezults2[id].append(naklimrez[id])
					eqprofcomislim2[id].append(ksdeloklim2[id] * comismaker)

				if mytradepositionbuy[id] != None:
					eqmytraderezults[id].append(naklimrez[id] + 100 * (dBid[sym1]- mytradepositionbuy[id]) / mytradepositionbuy[id])
					eqprofcomislim1[id].append(ksdeloklim1[id] * comismaker)
				if mytradepositionsell[id] != None:
					eqmytraderezults[id].append(naklimrez[id] + 100 * (mytradepositionsell[id] - dAsk[sym1]) / mytradepositionsell[id])
					eqprofcomislim1[id].append(ksdeloklim1[id] * comismaker)

				if mytradepositionbuy2[id] != None:
					eqmytraderezults2[id].append(naklimrez2[id] + 100 * (dBid[sym2] - mytradepositionbuy2[id]) / mytradepositionbuy2[id])
					eqprofcomislim2[id].append(ksdeloklim2[id] * comismaker)
				if mytradepositionsell2[id] != None:
					eqmytraderezults2[id].append(naklimrez2[id] + 100 * (mytradepositionsell2[id] -dAsk[sym2]) / mytradepositionsell2[id])
					eqprofcomislim2[id].append(ksdeloklim2[id] * comismaker)

		#  TUT NADO VOYAT
		# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
		for onetwo in onetwomas:
			sym1 = onetwo[0]
			sym2 = onetwo[1]
			if sym1 in data and sym2 in data:
				if data[sym1]['dat'] != None and data[sym2]['dat'] != None:
					if data[sym1]['tmstp'][2] and data[sym2]['tmstp'][2]:

						Ask1 = data[sym1]['dat'][0]
						Bid1 = data[sym1]['dat'][1]
						Ask2 = data[sym2]['dat'][0]
						Bid2 = data[sym2]['dat'][1]

						Ask1f = futuredata[sym1]['dat'][0]
						Bid1f = futuredata[sym1]['dat'][1]
						Ask2f = futuredata[sym2]['dat'][0]
						Bid2f = futuredata[sym2]['dat'][1]

						dAsk [sym1]=Ask1
						dBid[sym1]= Bid1
						dAsk[sym2] = Ask2
						dBid[sym2] = Bid2

						dAskf[sym1] = Ask1f
						dBidf[sym1] = Bid1f
						dAskf[sym2] = Ask2f
						dBidf[sym2] = Bid2f

						#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
						for persr in persrs:
							id0= sym1 + '@' + sym2 + '@' + str(persr)
							# обзначим разрывы больше средней* tradevozobnov
							# ****************************************
							if totrade[id0] and (data[sym1]['tmstp'][1] > persr * traderazryv or data[sym2]['tmstp'][1] > persr * traderazryv):
								print(' RAZRIV ', day, ' ', exem.hr)
								counttotrade[id0] = 0
								totrade[id0] = False
							counttotrade[id0] += 1
							if totrade[id0] == False and counttotrade[id0] > persr * tradevozobnov:
								totrade[id0] = True
							#****************************************

							sredn1 = scie.getshlifmed_easy((Ask1 + Bid1) / 2,'1'+id0 , persr)
							sredn2 = scie.getshlifmed_easy((Ask2 + Bid2) / 2, '2'+id0, persr)
							if sredn1 != None and sredn2 != None:
								Asksp = 100 * Ask1 / sredn1 - 100 * Bid2 / sredn2
								Bidsp = 100 * Bid1 / sredn1 - 100 * Ask2 / sredn2
								# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
								for kperso in kpersos:
									id = sym1 + '@' + sym2 + '@' + str(persr) + '@' + str(kperso)
									So = scie.getshlifmed_easy(max(abs(Asksp), abs(Bidsp)),  'So'+id, persr * kperso)
									if So != None:
										# ************************************************
										SoAsk = So
										SoBid = 0 - So

										# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
										for ksovh in ksovhs:
											# ************************************************
											# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
											for koefvih in koefvihs:
												id= sym1 + '@' + sym2 + '@' + str(persr) + '@' + str(kperso) + '@' + str(ksovh) + '@' + str(koefvih)

												# ************************************************
												ct[id] += 1
												paintdictixes[id].append(ct[id])
												paintdictasksspread[id].append(Asksp)
												paintdictbidsspread[id].append(Bidsp)
												paintdictaskot[id].append(SoAsk * ksovh)
												paintdictbidot[id].append(SoBid * ksovh)

												ksovih = ksovh * koefvih
												#1111111111111111111111111111111111111111111111111111111111
												# блок исполнения    отложек
												if mytradesellimit[id]  != None and mytradesellimit[id]  < Bid1:
													mytradepositionsell[id]  = mytradesellimit[id]
													mytradesellimit[id]  = None
													if mytradepositionbuy[id]  != None:
														naklimrez[id] += 100 * (mytradepositionsell[id] - mytradepositionbuy[id] ) / mytradepositionbuy [id]
														mytraderezults[id] .append(naklimrez[id] )
														mytradepositionbuy[id]  = None
														ksdeloklim1[id]+=1
												if mytradebuylimit[id]  != None and mytradebuylimit[id]  > Ask1:
													mytradepositionbuy[id]  = mytradebuylimit [id]
													mytradebuylimit[id]  = None
													if mytradepositionsell[id]  != None:
														naklimrez[id]  += 100 * (mytradepositionsell[id]  - mytradepositionbuy[id] ) / mytradepositionsell[id]
														mytraderezults[id] .append(naklimrez[id] )
														mytradepositionsell[id]  = None
														ksdeloklim1[id] += 1
												# ************************************************
												#   блок установки отложек
												if So > minkso and totrade[id0]:
													if mytradesellimit[id] == None and mytradepositionsell[id] == None and Bidsp > SoAsk * ksovh:
														mytradesellimit[id] = (Bid1 + Ask1) / 2
													if mytradebuylimit[id] == None and mytradepositionbuy[id] == None and Asksp < SoBid * ksovh:
														mytradebuylimit[id] = (Bid1 + Ask1) / 2
												# ************************************************
												#   блок снятия отложек
												if mytradesellimit[id] != None and Asksp < SoAsk * ksovh * 0.7:
													mytradesellimit[id] = None
												if mytradebuylimit[id] != None and Bidsp > SoBid * ksovh * 0.7:
													mytradebuylimit[id] = None
												# ************************************************
												# 22222222222222222222222222222222222222222222
												# ************************************************
												# блок исполнения    отложек
												if mytradesellimit2[id] != None and mytradesellimit2[id] < Bid2:
													mytradepositionsell2[id] = mytradesellimit2[id]
													mytradesellimit2[id] = None
													if mytradepositionbuy2[id] != None:
														naklimrez2[id] += 100 * (mytradepositionsell2[id] - mytradepositionbuy2[id]) / mytradepositionbuy2[id]
														mytraderezults2[id].append(naklimrez2[id])
														mytradepositionbuy2[id] = None
														ksdeloklim2[id] += 1
												if mytradebuylimit2[id] != None and mytradebuylimit2[id] > Ask2:
													mytradepositionbuy2[id] = mytradebuylimit2[id]
													mytradebuylimit2[id] = None
													if mytradepositionsell2[id] != None:
														naklimrez2[id] += 100 * (mytradepositionsell2[id] - mytradepositionbuy2[id]) / mytradepositionsell2 [id]
														mytraderezults2[id].append(naklimrez2[id])
														mytradepositionsell2[id] = None
														ksdeloklim2[id] += 1
												# ************************************************
												#   блок установки отложек
												if So > minkso and totrade[id0]:
													if mytradesellimit2[id] == None and mytradepositionsell2[id] == None and Asksp < SoBid * ksovh:
														mytradesellimit2[id] = (Bid2 + Ask2) / 2
													if mytradebuylimit2[id] == None and mytradepositionbuy2[id] == None and Bidsp > SoAsk * ksovh:
														mytradebuylimit2[id] = (Bid2 + Ask2) / 2
												# ************************************************
												#   блок снятия отложек
												if mytradesellimit2[id] != None and Bidsp > SoBid * ksovh * 0.7:
													mytradesellimit2[id] = None
												if mytradebuylimit2[id] != None and Asksp < SoAsk * ksovh * 0.7:
													mytradebuylimit2[id] = None

												# ************************************************
												# ************************************************
												# ************************************************
												# ************************************************
												# продажа
												if Bidsp > SoAsk * ksovh and flagsell[id] and So > minkso and totrade[id0]:  # and (So1-So2) >So/2:
													flagsell[id] = False
													flagsellvih[id] = True
													sellopenprice1[id] = Bid1
													buyopenprice2[id] = Ask2
													sellopenprice1f[id] = Bid1f
													buyopenprice2f[id] = Ask2f

													volamaxsell1[id]  = -100
													volaminsell1[id]  = 1000000000
													volamaxbuy2[id]  = -100
													volaminbuy2[id]  = 1000000000

												volamaxsell1[id]  = max(volamaxsell1[id] , Ask1)
												volaminsell1[id]  = min(volaminsell1[id] , Bid1)
												volamaxbuy2[id]  = max(volamaxbuy2[id] , Ask2)
												volaminbuy2 [id] = min(volaminbuy2[id] , Bid2)

												# закрытие продажи  покупкой
												if Asksp < SoBid * ksovih and flagsellvih[id] and totrade[id0]:  # Asksp<SoBid
													flagsellvih[id] = False
													flagsell[id] = True
													sellcloseprice1[id] = Ask1
													buycloseprice2[id] = Bid2
													sellcloseprice1f[id] = Ask1f
													buycloseprice2f[id] = Bid2f
													profit1 = 100 * (sellopenprice1[id] - sellcloseprice1[id]) / sellopenprice1[id]
													profit2= 100 * (buycloseprice2[id] - buyopenprice2[id]) / buyopenprice2[id]
													profit1f = 100 * (sellopenprice1f[id] - sellcloseprice1f[id]) / sellopenprice1f[id]
													profit2f = 100 * (buycloseprice2f[id] - buyopenprice2f[id]) / buyopenprice2f[id]
													nakprofrez1[id] += profit1
													nakprofrez2[id] += profit2
													nakprofrez1f[id] += profit1f
													nakprofrez2f[id] += profit2f

													vola1 = 100 * (volamaxsell1[id]  - volaminsell1[id] ) / sellopenprice1[id]
													vola2 = 100 * (volamaxbuy2[id]  - volaminbuy2[id] ) / buyopenprice2[id]
													nakotnvola1[id]  += 100 * profit1 / vola1
													nakotnvola2[id]  += 100 * profit2 / vola2
													masotnvola1[id] .append(nakotnvola1[id] )
													masotnvola2[id] .append(nakotnvola2[id] )

													countprofrezixes[id]  += 1
													profrezixes[id] .append(countprofrezixes[id] )

													profrez1[id].append(nakprofrez1[id])
													profrez2[id].append(nakprofrez2[id])
													profrezall[id].append(nakprofrez1[id] + nakprofrez2[id])

													profrez1f[id].append(nakprofrez1f[id])
													profrez2f[id].append(nakprofrez2f[id])
													profrezallf[id].append(nakprofrez1f[id] + nakprofrez2f[id])

													ksdelok[id] += 1
													profcomis[id].append(ksdelok[id]*comis)

												# покупка
												if Asksp < SoBid * ksovh and flagbuy[id] and So > minkso and totrade[id0]:  # and (So1-So2) >So/2:
													flagbuy[id] = False
													flagbuyvih[id] = True
													buyopenprice1[id] = Ask1
													sellopenprice2[id] = Bid2
													buyopenprice1f[id] = Ask1f
													sellopenprice2f[id] = Bid2f

													volamaxbuy1[id]  = -100
													volaminbuy1[id]  = 1000000000
													volamaxsell2[id]  = -100
													volaminsell2[id]  = 1000000000

												volamaxbuy1[id]  = max(volamaxbuy1[id] , Ask1)
												volaminbuy1[id]  = min(volaminbuy1[id] , Bid1)
												volamaxsell2[id]  = max(volamaxsell2[id] , Ask2)
												volaminsell2[id]  = min(volaminsell2[id] , Bid2)

												# закрытие покупки продажей
												if Bidsp > SoAsk * ksovih and flagbuyvih[id] and totrade[id0]:  # Bidsp>SoAsk
													flagbuyvih[id] = False
													flagbuy[id] = True
													buycloseprice1[id] = Bid1
													sellcloseprice2[id] = Ask2
													buycloseprice1f[id] = Bid1f
													sellcloseprice2f[id] = Ask2f
													profit1 = 100 * (buycloseprice1[id] - buyopenprice1[id]) / buyopenprice1[id]
													profit2 = 100 * (sellopenprice2[id] - sellcloseprice2[id]) / sellopenprice2[id]
													profit1f = 100 * (buycloseprice1f[id] - buyopenprice1f[id]) / buyopenprice1f [id]
													profit2f = 100 * (sellopenprice2f[id] - sellcloseprice2f[id]) / sellopenprice2f[id]
													nakprofrez1[id] += profit1
													nakprofrez2[id] += profit2
													nakprofrez1f[id] += profit1f
													nakprofrez2f[id] += profit2f

													vola1 = 100 * (volamaxbuy1[id] - volaminbuy1[id]) / buyopenprice1[id]
													vola2 = 100 * (volamaxsell2[id] - volaminsell2[id]) / sellopenprice2[id]
													nakotnvola1[id] += 100 * profit1 / vola1
													nakotnvola2[id] += 100 * profit2 / vola2
													masotnvola1[id].append(nakotnvola1[id])
													masotnvola2[id].append(nakotnvola2[id])


													countprofrezixes[id] += 1
													profrezixes[id].append(countprofrezixes[id])

													profrez1[id].append(nakprofrez1[id])
													profrez2[id].append(nakprofrez2[id])
													profrezall[id].append(nakprofrez1[id] + nakprofrez2[id])

													profrez1f[id].append(nakprofrez1f[id])
													profrez2f[id].append(nakprofrez2f[id])
													profrezallf[id].append(nakprofrez1f[id] + nakprofrez2f[id])

													ksdelok[id] += 1
													profcomis[id].append(ksdelok[id]*comis)
									# ************************************************


	# except:
	except Exception:
		print(traceback.format_exc())
		print('error')
		break




# print('PAINT', sym1, "  ", sym2,'   ',persrs)
print(f'time = {time.time() - timer}')
# for persr,kperso,ksovh,koefvih in itertools.product(persrs, kpersos,ksovhs,koefvihs ):
for onetwo, persr, kperso, ksovh, koefvih in itertools.product(onetwomas, persrs, kpersos, ksovhs, koefvihs):
	sym1 = onetwo[0]
	sym2 = onetwo[1]
	id = sym1 + '@' + sym2 + '@' + str(persr) + '@' + str(kperso) + '@' + str(ksovh) + '@' + str(koefvih)
	color = get_color()
	fig = px.line( 	title=f"D id {id}  ")
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
	fig.add_scatter(x=profrezixes[id], y=mytraderezults[id], line_color=clr, name=' Limit rezults')
	clr = color()
	fig.add_scatter(x=profrezixes[id], y=mytraderezults2[id], line_color=clr, name=' Limit rezults2')
	clr = color()
	fig.add_scatter(x=profrezixes[id], y=profcomis[id], line_color=clr, name='comis')
	fig.show()

	color = get_color()
	fig = px.line( 	title=f"D id {id}  ")
	fig.add_scatter(x=profrezixes[id], y=masotnvola1[id], line_color=clr, name=sym1 + 'nakotnvola1')
	clr = color()
	fig.add_scatter(x=profrezixes[id], y=masotnvola2[id], line_color=clr, name=sym2 + ' nakotnvola2')
	clr = color()
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
	fig.add_scatter(x=eqprofrezixes, y=eqmytraderezults[id], line_color=clr, name=' eqLimit rezults')
	clr = color()
	fig.add_scatter(x=eqprofrezixes, y=eqmytraderezults2[id], line_color=clr, name=' eqLimit rezults2')
	clr = color()
	fig.add_scatter(x=eqprofrezixes, y=eqprofcomislim1[id], line_color=clr, name=' eqprofcomislim1')
	clr = color()
	fig.add_scatter(x=eqprofrezixes, y=eqprofcomislim2[id], line_color=clr, name=' eqprofcomislim2')

	clr = color()
	fig.add_scatter(x=eqprofrezixes, y=eqprofcomis[id], line_color=clr, name='eqcomis')
	fig.show()
	
	# color = get_color()
	# fig = px.line( 	title=f"D id {id}  ")
	# clr = color()
	# fig.add_scatter(x=paintdictixes[id], y=paintdictasksspread[id], line_color=clr, name= ' askSpread')
	# fig.add_scatter(x=paintdictixes[id], y=paintdictbidsspread[id], line_color=clr, name=' bidSpread')
	# clr = color()
	# fig.add_scatter(x=paintdictixes[id], y=paintdictaskot[id] ,line_color=clr, name=' askot')
	# fig.add_scatter(x=paintdictixes[id], y=paintdictbidot[id], line_color=clr, name=' bidot')
	# fig.show()
