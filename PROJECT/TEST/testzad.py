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

# mysyms = {'GD', 'SV', 'BR', 'NG', 'W4', 'Eu', 'Si', 'MX','ED','SR','SP'}
# myklaster = ['MAIN', 'NEAR', 'USAFUT', 'FAR']
myklaster = ['MAIN', 'NEAR']
mysyms = ['GD']

markets = ['MOEX2', 'FRTS2', 'CURcross', 'USAFUT', 'CUR', 'RAW', 'FxMETBR', 'FxCUR']
# markets = ['FRTS2', 'FxMETBR', 'USAFUT', 'CUR', 'RAW', 'FxCUR']  # ,'MOEX'
instdict = dict()

minutki = 0
onlymerge = 0

# sym1='SiH4*FRTS2'
# sym1='SiM4*FRTS2'
# sym1='SiU4*FRTS2'
# sym2='USD000UTSTOM*CUR'
# sym2='USD000000TOD*CUR'
# sym2= 'USDRUBF*FRTS2'

# sym1='EDH4*FRTS2'
# sym2='EDM4*FRTS2'
# sym2= 'EURUSD*FxCUR'

# sym1='GDM4*FRTS2'
# sym1='GDU4*FRTS2'
# sym1='FUTGCG24.US*USAFUT'
sym1='Золото*RAW'
# sym1='XAUUSD*FxMETBR'
# sym2= 'GDH4*FRTS2'
# sym2='GLDRUBF*FRTS2'
# sym2='Золото*RAW'
sym2='XAUUSD*FxMETBR'

# sym1='MXM4*FRTS2'
# sym1='MXH4*FRTS2'
# sym2= 'IMOEXF*FRTS2'

# sym1 = 'Природный газ*RAW'
# sym1 = 'NGF4*FRTS2'
# sym1='NGH4*FRTS2'
# sym1='FUTQGH24.US*USAFUT'

# sym2='NGG4*FRTS2'
# sym2 = 'Природный газ*RAW'
# sym2='NatGas*FxMETBR'
# discret=False


showspread = True
zaderzka=3
comis = 0.03
persr = 3000 # период средней
kperso = 3 # период СКО = persr *kperso
ksovh = 0.5
ksovih = 0.5
minkso = 0


start_year, start_month, start_day, start_hour = 2024, 1, 14, 4
sstop_year, sstop_month, sstop_day, sstop_hour = 2024, 1, 19, 20

content = getdata_merge(onlymerge, minutki, markets, 'G:\\DATA_SBOR', start_year, start_month, start_day, start_hour, sstop_year,
						sstop_month, sstop_day, sstop_hour)
print(content)

exem = Getl2(content, 200, 0.95, 5)

scie = Mysredndiskret(300)


z = exem.get_l2NEW()  # получает словарь котиров
day0 = -1
count = 0
ct = -1

razrez = 0
countrr = 0

paintdict = {}
# подготовка словаря отрисовки
# FUT6EH24.US*USAFUT
# EDH4*FRTS2

# sym1='GLDRUBF*FRTS2'
# sym2='XAUUSD*FxMETBR'

# sym1='NatGas*FxMETBR'
# sym2='NGF4*FRTS2'


paintdict[sym1] = dict()
paintdict[sym1]['asksspread'] = []
paintdict[sym1]['bidsspread'] = []
paintdict[sym1]['ixes'] = []
paintdict[sym1]['askot'] = []
paintdict[sym1]['bidot'] = []



profrez1 = []
profrez2 = []
profrezall = []
profrez1f = []
profrez2f = []
profrezallf = []
profrezixes = []
profcomis = []
nakprofrez1 = 0
nakprofrez2 = 0
nakprofrez1f = 0
nakprofrez2f = 0
nakcomis = 0
countprofrezixes = -1

flagsell = True
flagbuy = True
flagsellvih = False
flagbuyvih = False
# paintdict[sym2] = dict()
# paintdict[sym2]['asksspread']=[]
# paintdict[sym2]['bidsspread']=[]


baza= deque()

for i in range(zaderzka):
	data0 = next(z).copy()
	baza.append(data0)
	# print(i,data)

# print(len(baza))
# for i in baza:
# 	print(i)
while True:

	count += 1
	try:
		# timer=time.time()
		futuredata= next(z).copy()  # это якобы на серваке - к нему нужен доступ
		baza.append(futuredata)
		data=baza.popleft()


		# if data!=futuredata:
		# 	print('futuredata ', futuredata)
		# 	print('data ', data)

		tme = exem.ttime  # Эмуляция получения времени
		day = exem.day
		#  эмуляция получения списка инструментов  раз в день
		if day != day0:
			day0 = day
			year = exem.year
			month = exem.mon

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


					sredn1 = scie.getshlifmed_easy((Ask1 + Bid1) / 2, sym1, persr)
					sredn2 = scie.getshlifmed_easy((Ask2 + Bid2) / 2, sym2, persr)
					if sredn1 != None and sredn2 != None:


						Asksp = 100 * Ask1 / sredn1 - 100 * Bid2 / sredn2
						Bidsp = 100 * Bid1 / sredn1 - 100 * Ask2 / sredn2
						So = scie.getshlifmed_easy(max(abs(Asksp), abs(Bidsp)), sym1 + 'So', persr * kperso)


						if So != None:

							ct += 1
							paintdict[sym1]['ixes'].append(ct)
							paintdict[sym1]['asksspread'].append(Asksp)
							paintdict[sym1]['bidsspread'].append(Bidsp)



							SoAsk = So
							SoBid = 0 - So
							paintdict[sym1]['askot'].append(SoAsk* ksovh)
							paintdict[sym1]['bidot'].append(SoBid* ksovh)

							# продажа
							if Bidsp > SoAsk * ksovh and flagsell and So> minkso :  #and (So1-So2) >So/2:
								flagsell = False
								flagsellvih = True
								sellopenprice1 = Bid1
								buyopenprice2 = Ask2
								sellopenprice1f = Bid1f
								buyopenprice2f = Ask2f

							# закрытие продажи  покупкой
							if Asksp < SoBid * ksovih and flagsellvih:  # Asksp<SoBid
								flagsellvih = False
								flagsell = True
								sellcloseprice1 = Ask1
								buycloseprice2 = Bid2
								sellcloseprice1f = Ask1f
								buycloseprice2f = Bid2f
								profit1 = 100 * (sellopenprice1 - sellcloseprice1) / sellopenprice1
								profit2 = 100 * (buycloseprice2 - buyopenprice2) / buyopenprice2

								profit1f = 100 * (sellopenprice1f - sellcloseprice1f) / sellopenprice1f
								profit2f = 100 * (buycloseprice2f - buyopenprice2f) / buyopenprice2f

								countprofrezixes += 1
								profrezixes.append(countprofrezixes)
								nakprofrez1 += profit1
								profrez1.append(nakprofrez1)
								nakprofrez2 += profit2
								profrez2.append(nakprofrez2)
								profrezall.append(nakprofrez1 + nakprofrez2)

								nakprofrez1f += profit1f
								profrez1f.append(nakprofrez1f)
								nakprofrez2f += profit2f
								profrez2f.append(nakprofrez2f)
								profrezallf.append(nakprofrez1f + nakprofrez2f)


								nakcomis += comis
								profcomis.append(nakcomis)



							# покупка
							if Asksp < SoBid * ksovh and flagbuy and So> minkso : #and (So1-So2) >So/2:
								flagbuy = False
								flagbuyvih = True
								buyopenprice1 = Ask1
								sellopenprice2 = Bid2
								buyopenprice1f = Ask1f
								sellopenprice2f = Bid2f

							# закрытие покупки продажей
							if Bidsp > SoAsk * ksovih and flagbuyvih:  # Bidsp>SoAsk
								flagbuyvih = False
								flagbuy = True
								buycloseprice1 = Bid1
								sellcloseprice2 = Ask2
								buycloseprice1f = Bid1f
								sellcloseprice2f = Ask2f
								profit1 = 100 * (buycloseprice1 - buyopenprice1) / buyopenprice1
								profit2 = 100 * (sellopenprice2 - sellcloseprice2) / sellopenprice2
								profit1f = 100 * (buycloseprice1f - buyopenprice1f) / buyopenprice1f
								profit2f = 100 * (sellopenprice2f - sellcloseprice2f) / sellopenprice2f

								countprofrezixes += 1
								profrezixes.append(countprofrezixes)
								nakprofrez1 += profit1
								profrez1.append(nakprofrez1)
								nakprofrez2 += profit2
								profrez2.append(nakprofrez2)
								profrezall.append(nakprofrez1 + nakprofrez2)

								nakprofrez1f += profit1f
								profrez1f.append(nakprofrez1f)
								nakprofrez2f += profit2f
								profrez2f.append(nakprofrez2f)
								profrezallf.append(nakprofrez1f + nakprofrez2f)


								nakcomis += comis
								profcomis.append(nakcomis)


	# except:
	except Exception:
		print(traceback.format_exc())
		print('error')
		break

print('PAINT', sym1, "  ", sym2)
#
if showspread:
	color = get_color()
	fig = px.line(
		title=f"D n SPREAD {sym1} {sym2}   persr={persr}   kperso={kperso}  ksovh ={ksovh}  ksovih ={ksovih}   minkso={minkso}   ")

	clr = color()
	fig.add_scatter(x=paintdict[sym1]['ixes'], y=paintdict[sym1]['asksspread'], line_color=clr, name=sym1 + " - " + sym2 + ' ask')
	fig.add_scatter(x=paintdict[sym1]['ixes'], y=paintdict[sym1]['bidsspread'], line_color=clr, name=sym1 + " - " + sym2 + ' bid')

	clr = color()
	fig.add_scatter(x=paintdict[sym1]['ixes'], y=paintdict[sym1]['askot'], line_color=clr, name=' askot')
	fig.add_scatter(x=paintdict[sym1]['ixes'], y=paintdict[sym1]['bidot'], line_color=clr, name=' bidot')

	fig.show()


color = get_color()
fig = px.line(
	title=f"D REZ {sym1} {sym2}  persr={persr}   kperso={kperso}  ksovh ={ksovh}  ksovih ={ksovih}   minkso={minkso}   zaderzka={zaderzka} " )
clr = color()
fig.add_scatter(x=profrezixes, y=profrez1, line_color=clr, name=sym1 + " - " + ' profrez1')
clr = color()
fig.add_scatter(x=profrezixes, y=profrez2, line_color=clr, name=sym2 + " - " + ' profrez2')
clr = color()
fig.add_scatter(x=profrezixes, y=profrezall, line_color=clr, name=' profrezall')
clr = color()
fig.add_scatter(x=profrezixes, y=profrez1f, line_color=clr, name=sym1 + " - " + ' profrez1f')
clr = color()
fig.add_scatter(x=profrezixes, y=profrez2f, line_color=clr, name=sym2 + " - " + ' profrez2f')
clr = color()
fig.add_scatter(x=profrezixes, y=profrezallf, line_color=clr, name=' profrezallf')

clr = color()
fig.add_scatter(x=profrezixes, y=profcomis, line_color=clr, name='comis')
fig.show()

