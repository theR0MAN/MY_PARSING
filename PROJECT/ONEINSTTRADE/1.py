from PROJECT.TEST.Test_lib import *
from PROJECT.VIZUAL.Viz_lib import get_color
from PROJECT.SCIENTIC.sc_sredn_lib import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from platform import system
import plotly.express as px
from collections import deque
import datetime, time  # timer=time.time()
import traceback
from statistics import mean
flaglong=True
flagshort=True

markets = ['FRTS']  # ,'MOEX'
minutki = 0
onlymerge = 0
vizinst='BR'
x = 0
ixmas = []
superaskmas = []
superbidmas = []
datamas=dict()
# instrument2 = 'Si-3.24*FRTS'
# instrument3 = 'Si-6.24*FRTS'

instrument = 'Si-3.24*FRTS'
instrument2 = 'GOLD-3.24*FRTS'
instrument3 = 'GOLD-6.24*FRTS'

# instrument = 'NG-9.23*FRTS'
# instrument2 = 'NG-10.23*FRTS'
# instrument3 = 'NG-11.23*FRTS'

start_year, start_month, start_day, start_hour = 2023, 10, 6, 10
stop_year, stop_month, stop_day, stop_hour = 	 2023, 10, 12, 17

getpath = 'G:\\DATA_SBOR' if system() == 'Windows' else '/media/roman/J/DATA_SBOR'
content = getdata_merge(onlymerge, minutki, markets, getpath, start_year, start_month, start_day, start_hour, stop_year,
						stop_month, stop_day, stop_hour)
print(content)

bazmas = []
askmas = []
bidmas = []

ylongmas = []
yshortmas = []

xlongmas = []
xshortmas = []

comisaskmas = []
comisbidmas = []

askotklmas = []
bidotklmas = []
askmas2 = []
bidmas2 = []
askmas3 = []
bidmas3 = []
srexpmas = []
sreasymas = []
medmas = []
shlifmedmas = []
shlifmedmas2 = []
shlifmedmas20 = []

tm = 0
# z = get_l2(content)

heart = Myheartbeat(100, 50, 0.95, 5)
exem = Getl2(content)
scie = Mysredn()
skot = exem.get_l2()  # получает словарь котиров
# countdict = dict()  # через какой промежуток брать медиану
day0 = -1
dt = dict()
# kstk = dict()
alltotrade=dict()
kso=1
total=0
# koefdict=dict()
medper = 0
A = dict()
B = dict()
baza = dict()
bazafin = dict()
bazasred = dict()
bazaso = dict()

# mascen=[]
# ln=0
# sc=0
# longvh = 100 * ((RMED - Ask) - Akoefin * (Ask - Bid)) / Ask - (comis + forain);
# shortvh = 100 * ((Bid - RMED) - Akoefin * (Ask - Bid)) / Ask - (comis + forain);
# longout = 100 * ((RMED - Ask) - Akoefout * (Ask - Bid)) / Ask - (comis + foraout);
# shortout = 100 * ((Bid - RMED) - Akoefout * (Ask - Bid)) / Ask - (comis + foraout);

Akoefin=0.5

persec = 25
medperiod = 100
comis=0.03
forain=0.01

limsig=2

deals=dict()
once =True
while True:
	try:
		dt0 = next(skot)  # это якобы на серваке - к нему нужен доступ
		tme = exem.ttime  # Эмуляция получения времени
		# print(tme)
		day = exem.day
		#  эмуляция получения списка инструментов  раз в день
		if day != day0:
			day0 = day
			dt = dict()
			kstk = dict()
			spisinstr = list()
			for key in dt0:
				spisinstr.append(key)
			# получения списка только фьючей и  минимум парных, игрорируя индексы и прочую дичь
			A, B = get_fut(spisinstr)
			for key in A:
				if key not in deals:
					deals[key] = dict()
					deals[key]["profit"] = 0
					deals[key]["flagshort"] = True
					deals[key]["flaglong"] = True
					deals[key]["lastlong"] = None
					deals[key]["lastshort"] = None
			# D=dict()
			print(A)
			print(B)
			for key in B:
				alltotrade[key]=dict()
				alltotrade[key]['instruments'] = dict()
				for i in B[key]:
					alltotrade[key]['instruments'] [i]=dict()
					# инициализируем датасловарь
					if key == vizinst:
						if i not in datamas:
							datamas[i] = dict()
							datamas[i]['asks'] = []
							datamas[i]['bids'] = []



		#  нужно заполнить список инструменов  дня
		for key in A:
			dt[key] = dt0[key]
		# 	получение ( хертбит) на основе  инструменов  дня
		H = heart.get_heartbeats(dt, tme)
		# 	если мажор укладывается в хертбит считаем медианы через persec секунд
		if medper < persec:
			medper += 1
		else:
			medper = 0
			for key in B:
				if H[B[key][0]]:
					yes = True
					for i in B[key]:
						# сперва проверка на нормальность  всех котиров фьючей с общей базой для кореектной синхронизации медианы
						if dt[i]['asks'] == [] or dt[i]['bids'] == []:
							yes = False
					# если всё ок
					if yes:
						for i in B[key]:
							Ask = dt[i]['asks'][0][0]
							Bid = dt[i]['bids'][0][0]
							data = (Ask + Bid) / 2
							mediana = scie.getshlifmed_exp(data, i, medperiod)
							if mediana != None:
								# заполнение корректировочных кэфов по каждому инструменту
								baza[i] = 100 / mediana
		z=dict()
		for key in B:
			mascen = []
			if B[key][0] in baza:
				for i in B[key]:
					z[i]=dict()
					z[i]['asks']=[]
					z[i]['bids']=[]
					# перемножить все цены на кэфы и впаковать в суперстакан доп
					for k in dt[i]['asks']:
						z[i]['asks'].append([k[0]*baza[i],k[1]])
					for k in dt[i]['bids']:
						z[i]['bids'].append([k[0]*baza[i],k[1]])
					mascen.append(z[i])
					alltotrade[key]['instruments'] [i]['ask']=z[i]['asks'][0][0]
					alltotrade[key]['instruments'] [i]['bid'] = z[i]['bids'][0][0]
				kstk=megamerge_stakan(mascen)
				alltotrade[key]['megaAsk']=kstk['asks'][0][0]
				alltotrade[key]['megaBid'] = kstk['bids'][0][0]
				for i in B[key]:
					alltotrade[key]['instruments'][i]['sigbuy']=alltotrade[key]['megaBid']-alltotrade[key]['instruments'] [i]['ask']
					alltotrade[key]['instruments'][i]['sigsell'] = alltotrade[key]['instruments'][i]['bid']-alltotrade[key] ['megaAsk']
		# alltotrade чисто для визуалки нужно
		# if 'megaAsk' in alltotrade['NG']:
		# 	print( alltotrade['NG']['megaAsk'],' * ',alltotrade['NG']['megaBid'] ,'     ', alltotrade['NG']['instruments'] ['NG-12.23*FRTS']['ask'],' * ',alltotrade['NG']['instruments'] ['NG-12.23*FRTS']['bid'])
			# for i in  alltotrade['NG']['instruments']:


		if vizinst in alltotrade and 'megaBid' in alltotrade[vizinst]:
			x += 1
			ixmas.append(x)
			superaskmas.append(alltotrade[vizinst] ['megaAsk'])
			superbidmas.append(alltotrade[vizinst]['megaBid'])
			for key2 in alltotrade[vizinst]['instruments']:
				datamas[key2]['asks'].append (alltotrade[vizinst]['instruments'] [key2]['ask'])
				datamas[key2]['bids'].append(alltotrade[vizinst]['instruments'][key2]['bid'])




	except RuntimeError:
		print("StopIteration error handled successfully")
		break
	except Exception:
		traceback.print_exc()
		print('stop')
		break

# 	выведем эту радость
color = get_color()
fig = px.line()
clr = color()
fig.add_scatter(x=ixmas, y=superaskmas, line_color=clr, name= ' Mask')
fig.add_scatter(x=ixmas, y=superbidmas, line_color=clr, name= ' Mbid')

for inst in datamas:
	clr = color()
	fig.add_scatter(x=ixmas, y=datamas[inst]['asks'], line_color=clr, name=inst + ' ask')
	fig.add_scatter(x=ixmas, y=datamas[inst]['bids'], line_color=clr, name=inst + ' bid')
fig.show()