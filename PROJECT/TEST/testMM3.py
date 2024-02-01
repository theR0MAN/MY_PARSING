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

dats = {'Si': ['SiM4*FRTS2', 'USD000UTSTOM*CUR', 'SiU4*FRTS2']}
instdict = dict()

# sym1 = 'SiM4*FRTS2'
# sym2 = 'USD000UTSTOM*CUR'

zaderzka = 3
comis = 0.03
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

exem = Getl2(content, 300, 0.95, 5)
scie = Mysredndiskret(300)

z = exem.get_l2NEW()  # получает словарь котиров
day0 = -1



# persrs = [1000,2000,4000,8000]
# kpersos = [1,2,3] # период СКО = persr *kperso
# ksovhs = [1,1.3,1.9]
# koefvihs = [1]

persrs = [2000,4000]
kpersos = [2] # период СКО = persr *kperso
ksovhs = [1]
koefvihs = [1]



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
nakcomis =dict() 
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


# volamaxsell1 = -100
# volaminsell1 = 1000000000
# volamaxbuy1  =-100
# volaminbuy1 =  1000000000
# masotnvola1=[]
# nakotnvola1=0
#
# volamaxsell2 = -100
# volaminsell2 = 1000000000
# volamaxbuy2  =-100
# volaminbuy2 =  1000000000
# masotnvola2=[]
# nakotnvola2=0


sym1='SiM4*FRTS2'
sym2='USD000UTSTOM*CUR'
for persr,kperso,ksovh,koefvih in itertools.product(persrs, kpersos,ksovhs,koefvihs ):
	id = sym1 + '@' + sym2 + '@' + str(persr) + '@' + str(kperso) + '@' + str(ksovh) + '@' + str(koefvih)
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
	nakcomis [id] =  0
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

zadr = deque()
for i in range(zaderzka):
	data0 = next(z).copy()
	zadr.append(data0)
timer = time.time()
while True:
	try:
		# print(f'time = {time.time() - timer}')
		# timer = time.time()
		futuredata = next(z).copy()  # это якобы на серваке - к нему нужен доступ
		zadr.append(futuredata)
		data = zadr.popleft()

		tme = exem.ttime  # Эмуляция получения времени
		day = exem.day
		#  эмуляция получения списка инструментов  раз в день
		if day != day0:
			day0 = day
			year = exem.year
			month = exem.mon

		#  TUT NADO VOYAT
		# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
		if sym1 in data and sym2 in data:
			# identifikator = sym1 + '@' + sym2+ '@'

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

					#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
					for persr in persrs:
						id= sym1 + '@' + sym2 + '@' + str(persr)
						sredn1 = scie.getshlifmed_easy((Ask1 + Bid1) / 2,'1'+id , persr)
						sredn2 = scie.getshlifmed_easy((Ask2 + Bid2) / 2, '2'+id, persr)
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
											# блок исполнения    отложек
											if mytradesellimit[id]  != None and mytradesellimit[id]  < Bid1:
												mytradepositionsell[id]  = mytradesellimit[id]
												mytradesellimit[id]  = None
												if mytradepositionbuy[id]  != None:
													naklimrez[id] += 100 * (mytradepositionsell[id] - mytradepositionbuy[id] ) / mytradepositionbuy [id]
													mytraderezults[id] .append(naklimrez[id] )
													mytradepositionbuy[id]  = None
											if mytradebuylimit[id]  != None and mytradebuylimit[id]  > Ask1:
												mytradepositionbuy[id]  = mytradebuylimit [id]
												mytradebuylimit[id]  = None
												if mytradepositionsell[id]  != None:
													naklimrez[id]  += 100 * (mytradepositionsell[id]  - mytradepositionbuy[id] ) / mytradepositionsell[id]
													mytraderezults[id] .append(naklimrez[id] )
													mytradepositionsell[id]  = None
											# ************************************************
											#   блок установки отложек
											if So > minkso:
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

											if mytradebuylimit2[id] != None and mytradebuylimit2[id] > Ask2:
												mytradepositionbuy2[id] = mytradebuylimit2[id]
												mytradebuylimit2[id] = None
												if mytradepositionsell2[id] != None:
													naklimrez2[id] += 100 * (mytradepositionsell2[id] - mytradepositionbuy2[id]) / mytradepositionsell2 [id]
													mytraderezults2[id].append(naklimrez2[id])
													mytradepositionsell2[id] = None
											# ************************************************
											#   блок установки отложек
											if So > minkso:
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
											if Bidsp > SoAsk * ksovh and flagsell[id] and So > minkso:  # and (So1-So2) >So/2:
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
											if Asksp < SoBid * ksovih and flagsellvih[id]:  # Asksp<SoBid
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

												nakcomis[id] += comis
												profcomis[id].append(nakcomis[id])

											# покупка
											if Asksp < SoBid * ksovh and flagbuy[id] and So > minkso:  # and (So1-So2) >So/2:
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
											if Bidsp > SoAsk * ksovih and flagbuyvih[id]:  # Bidsp>SoAsk
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

												nakcomis[id] += comis
												profcomis[id].append(nakcomis[id])
								# ************************************************


	# except:
	except Exception:
		print(traceback.format_exc())
		print('error')
		break




print('PAINT', sym1, "  ", sym2,'   ',persrs)
print(f'time = {time.time() - timer}')
for persr,kperso,ksovh,koefvih in itertools.product(persrs, kpersos,ksovhs,koefvihs ):
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
	
	# color = get_color()
	# fig = px.line( 	title=f"D id {id}  ")
	# clr = color()
	# fig.add_scatter(x=paintdictixes[id], y=paintdictasksspread[id], line_color=clr, name= ' askSpread')
	# fig.add_scatter(x=paintdictixes[id], y=paintdictbidsspread[id], line_color=clr, name=' bidSpread')
	# clr = color()
	# fig.add_scatter(x=paintdictixes[id], y=paintdictaskot[id] ,line_color=clr, name=' askot')
	# fig.add_scatter(x=paintdictixes[id], y=paintdictbidot[id], line_color=clr, name=' bidot')
	# fig.show()
