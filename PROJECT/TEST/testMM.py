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
# markets = ['FRTS2']  # ,'MOEX'
instdict = dict()

minutki = 0
onlymerge = 0


sym1='SiM4*FRTS2'
sym2='USD000UTSTOM*CUR'


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
# sym1='Золото*RAW'
# sym1='XAUUSD*FxMETBR'
# sym2= 'GDH4*FRTS2'
# sym2='GLDRUBF*FRTS2'
# sym2='Золото*RAW'
# sym2='XAUUSD*FxMETBR'

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
persr = 4000# период средней
kperso = 2 # период СКО = persr *kperso
ksovh = 1
ksovih = 1
minkso =  comis

mytrade1=dict ()
mytrade1['sellimit']=None
mytrade1['buylimit']=None
mytrade1['positionbuy']=None
mytrade1['positionsell']=None
mytrade1['rezults']=[]
naklimrez=0

mytrade1['sellimit2']=None
mytrade1['buylimit2']=None
mytrade1['positionbuy2']=None
mytrade1['positionsell2']=None
mytrade1['rezults2']=[]
naklimrez2=0





start_year, start_month, start_day, start_hour = 2024, 1, 23, 4
sstop_year, sstop_month, sstop_day, sstop_hour = 2024, 1, 30, 20

content = getdata_merge(onlymerge, minutki, markets, 'G:\\DATA_SBOR', start_year, start_month, start_day, start_hour, sstop_year,
						sstop_month, sstop_day, sstop_hour)
print(content)

exem = Getl2(content, 300, 0.95, 5)

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



volamaxsell1 = -100
volaminsell1 = 1000000000
volamaxbuy1  =-100
volaminbuy1 =  1000000000
masotnvola1=[]
nakotnvola1=0

volamaxsell2 = -100
volaminsell2 = 1000000000
volamaxbuy2  =-100
volaminbuy2 =  1000000000
masotnvola2=[]
nakotnvola2=0



askm=[]
bidm=[]
sellimm=[]
buylimm=[]


# askm1=[]
# bidm1=[]
# sellimm1=[]
# buylimm1=[]

askm2=[]
bidm2=[]
sellimm2=[]
buylimm2=[]



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

timer=time.time()
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
							# ************************************************
							SoAsk = So
							SoBid = 0 - So
							paintdict[sym1]['askot'].append(SoAsk* ksovh)
							paintdict[sym1]['bidot'].append(SoBid* ksovh)
							# ************************************************
							askm.append(Ask1)
							bidm.append(Bid1)
							sellimm.append(mytrade1['sellimit'])
							buylimm.append(mytrade1['buylimit'])
							# ************************************************


							 # 11111111111111111111111111111111111111111111111111
							askm2.append(Ask2)
							bidm2.append(Bid2)
							sellimm2.append(mytrade1['sellimit2'])
							buylimm2.append(mytrade1['buylimit2'])
							# ************************************************
							# блок исполнения    отложек
							if mytrade1['sellimit']!=None and mytrade1['sellimit']<Bid1:
								mytrade1['positionsell'] =  mytrade1['sellimit']
								mytrade1['sellimit'] = None
								if mytrade1['positionbuy']!=None:
									naklimrez+=100 * (mytrade1['positionsell'] - mytrade1['positionbuy'] ) / mytrade1['positionbuy']
									mytrade1['rezults'].append(naklimrez)
									mytrade1['positionbuy'] = None


							if mytrade1['buylimit']!=None and mytrade1['buylimit']>Ask1:
								mytrade1['positionbuy'] =  mytrade1['buylimit']
								mytrade1['buylimit'] = None
								if mytrade1['positionsell']!=None:
									naklimrez += 100 * (mytrade1['positionsell'] - mytrade1['positionbuy'] ) / mytrade1['positionsell']
									mytrade1['rezults'].append(naklimrez)
									mytrade1['positionsell'] = None
							# ************************************************
							#   блок установки отложек
							if  So> minkso:
								if mytrade1['sellimit'] == None and mytrade1['positionsell'] == None and  Bidsp > SoAsk * ksovh:
									mytrade1['sellimit'] = (Bid1+Ask1)/2

								if mytrade1['buylimit'] == None and mytrade1['positionbuy'] == None and  Asksp < SoBid * ksovh:
									mytrade1['buylimit'] = (Bid1+Ask1)/2
							# ************************************************
							#   блок снятия отложек
							if mytrade1['sellimit'] != None and Asksp < SoAsk * ksovh*0.7:
								mytrade1['sellimit'] = None
							if mytrade1['buylimit'] != None and Bidsp > SoBid * ksovh*0.7:
								mytrade1['buylimit'] = None
								# ************************************************

							# 22222222222222222222222222222222222222222222
							askm2.append(Ask2)
							bidm2.append(Bid2)
							sellimm2.append(mytrade1['sellimit2'])
							buylimm2.append(mytrade1['buylimit2'])
							# ************************************************
							# блок исполнения    отложек
							if mytrade1['sellimit2'] != None and mytrade1['sellimit2'] < Bid2:
								mytrade1['positionsell2'] = mytrade1['sellimit2']
								mytrade1['sellimit2'] = None
								if mytrade1['positionbuy2'] != None:
									naklimrez2 += 100 * (mytrade1['positionsell2'] - mytrade1['positionbuy2']) / mytrade1['positionbuy2']
									mytrade1['rezults2'].append(naklimrez2)
									mytrade1['positionbuy2'] = None

							if mytrade1['buylimit2'] != None and mytrade1['buylimit2'] >  Ask2:
								mytrade1['positionbuy2'] = mytrade1['buylimit2']
								mytrade1['buylimit2'] = None
								if mytrade1['positionsell2'] != None:
									naklimrez2 += 100 * (mytrade1['positionsell2'] - mytrade1['positionbuy2']) / mytrade1['positionsell2']
									mytrade1['rezults2'].append(naklimrez2)
									mytrade1['positionsell2'] = None
							# ************************************************
							#   блок установки отложек
							if So > minkso:
								if mytrade1['sellimit2'] == None and mytrade1['positionsell2'] == None and Asksp < SoBid * ksovh:
									mytrade1['sellimit2'] = (Bid2 + Ask2) / 2

								if mytrade1['buylimit2'] == None and mytrade1['positionbuy2'] == None and   Bidsp > SoAsk * ksovh:
									mytrade1['buylimit2'] = (Bid2 + Ask2) / 2
							# ************************************************
							#   блок снятия отложек
							if mytrade1['sellimit2'] != None  and Bidsp > SoBid * ksovh*0.7:
								mytrade1['sellimit2'] = None
							if mytrade1['buylimit2'] != None  and Asksp < SoAsk * ksovh*0.7:
								mytrade1['buylimit2'] = None

							# ************************************************
							# ************************************************
							# ************************************************
							# ************************************************
							# продажа
							if Bidsp > SoAsk * ksovh and flagsell and So> minkso :  #and (So1-So2) >So/2:
								flagsell = False
								flagsellvih = True
								sellopenprice1 = Bid1
								buyopenprice2 = Ask2
								sellopenprice1f = Bid1f
								buyopenprice2f = Ask2f

								volamaxsell1 = -100
								volaminsell1 = 1000000000
								volamaxbuy2 = -100
								volaminbuy2 = 1000000000
		

							volamaxsell1 =max(volamaxsell1,Ask1)
							volaminsell1 =min(volaminsell1,Bid1)
							volamaxbuy2 = max(volamaxbuy2, Ask2)
							volaminbuy2 = min(volaminbuy2, Bid2)
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

								vola1=100 *(volamaxsell1-volaminsell1) / sellopenprice1
								vola2=100 *(volamaxbuy2-volaminbuy2) / buyopenprice2
								nakotnvola1+=100*profit1/ vola1
								nakotnvola2+=100*profit2/ vola2
								masotnvola1.append(nakotnvola1)
								masotnvola2.append(nakotnvola2)


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

								volamaxbuy1 = -100
								volaminbuy1 = 1000000000
								volamaxsell2 = -100
								volaminsell2 = 1000000000
								
							volamaxbuy1 = max(volamaxbuy1, Ask1)
							volaminbuy1 = min(volaminbuy1, Bid1)
							volamaxsell2 = max(volamaxsell2, Ask2)
							volaminsell2 = min(volaminsell2, Bid2)
				
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


								vola1= 100 * (volamaxbuy1  - volaminbuy1)/ buyopenprice1
								vola2=  100 * (volamaxsell2 - volaminsell2)/ sellopenprice2
								nakotnvola1 += 100 * profit1 / vola1
								nakotnvola2 += 100 * profit2 / vola2
								masotnvola1.append(nakotnvola1)
								masotnvola2.append(nakotnvola2)

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
						# ************************************************


	# except:
	except Exception:
		print(traceback.format_exc())
		print('error')
		break

print('PAINT', sym1, "  ", sym2)
print(f'time = {time.time()-timer}')
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


# color = get_color()
# fig = px.line( 	title=f"D REZ {sym1}   persr={persr}   kperso={kperso}  ksovh ={ksovh}  ksovih ={ksovih}   minkso={minkso}   zaderzka={zaderzka} " )
# clr = color()
# fig.add_scatter(x=paintdict[sym1]['ixes'], y=askm, line_color=clr, name=sym1 + " - " + ' askm')
# fig.add_scatter(x=paintdict[sym1]['ixes'], y=bidm, line_color=clr, name=sym1 + " - " + ' bidm')
# clr = color()
# fig.add_scatter(x=paintdict[sym1]['ixes'], y=sellimm, line_color=clr, mode='markers', name= ' sellimm')
# clr = color()
# fig.add_scatter(x=paintdict[sym1]['ixes'], y=buylimm, line_color=clr, mode='markers', name= ' buylimm')
# fig.show()
#
# color = get_color()
# fig = px.line( 	title=f"D REZ {sym2}  persr={persr}   kperso={kperso}  ksovh ={ksovh}  ksovih ={ksovih}   minkso={minkso}   zaderzka={zaderzka} " )
# clr = color()
# fig.add_scatter(x=paintdict[sym1]['ixes'], y=askm2, line_color=clr, name=sym2 + " - " + ' askm')
# fig.add_scatter(x=paintdict[sym1]['ixes'], y=bidm2, line_color=clr, name=sym2 + " - " + ' bidm')
# clr = color()
# fig.add_scatter(x=paintdict[sym1]['ixes'], y=sellimm2, line_color=clr, mode='markers', name= ' sellimm')
# clr = color()
# fig.add_scatter(x=paintdict[sym1]['ixes'], y=buylimm2, line_color=clr, mode='markers', name= ' buylimm')
# fig.show()


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
fig.add_scatter(x=profrezixes, y=mytrade1['rezults'], line_color=clr, name=' Limit rezults')
clr = color()
fig.add_scatter(x=profrezixes, y=mytrade1['rezults2'], line_color=clr, name=' Limit rezults2')
clr = color()
fig.add_scatter(x=profrezixes, y=profcomis, line_color=clr, name='comis')
fig.show()

color = get_color()
fig = px.line(
	title=f"D REZ {sym1} {sym2}  persr={persr}   kperso={kperso}  ksovh ={ksovh}  ksovih ={ksovih}   minkso={minkso}   zaderzka={zaderzka} " )
clr = color()
fig.add_scatter(x=profrezixes, y=masotnvola1, line_color=clr, name=sym1 + 'nakotnvola1')
clr = color()
fig.add_scatter(x=profrezixes, y=masotnvola2, line_color=clr, name=sym2 + ' nakotnvola2')
clr = color()
fig.show()


