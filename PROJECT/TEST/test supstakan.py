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
# instrument = 'Si-12.23*FRTS'
# instrument2 = 'Si-3.24*FRTS'
# instrument3 = 'Si-6.24*FRTS'

instrument = 'Si-3.24*FRTS'
instrument2 = 'GOLD-3.24*FRTS'
instrument3 = 'GOLD-6.24*FRTS'

# instrument = 'NG-9.23*FRTS'
# instrument2 = 'NG-10.23*FRTS'
# instrument3 = 'NG-11.23*FRTS'

start_year, start_month, start_day, start_hour = 2023, 10, 6, 14
stop_year, stop_month, stop_day, stop_hour = 	 2023, 10, 19, 15

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
ixmas = []
tm = 0
# z = get_l2(content)
x = 0
heart = Myheartbeat(100, 50, 0.95, 5)
exem = Getl2(content)
scie = Mysredn()
z = exem.get_l2()  # получает словарь котиров
# countdict = dict()  # через какой промежуток брать медиану
day0 = -1
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

while True:
	try:
		dt0 = next(z)  # это якобы на серваке - к нему нужен доступ
		tme = exem.ttime  # Эмуляция получения времени
		# print(tme)
		day = exem.day
		#  эмуляция получения списка инструментов  раз в день
		if day != day0:
			day0 = day
			spisinstr = list()
			for key in dt0:
				spisinstr.append(key)
			# получения списка только фьючей и  минимум парных, игрорируя индексы и прочую дичь
			A, B = get_fut(spisinstr)
			# D=dict()
			print(A)
			print(B)

		#  нужно заполнить список фильтрованных инструменов
		dt = dict()
		for key in A:
			dt[key] = dt0[key]
			if key not in deals:
				deals[key] = dict()
				deals[key]["profit"]=0
				deals[key]["flagshort"] = True
				deals[key]["flaglong"] = True
				deals[key]["lastlong"]=None
				deals[key]["lastshort"]=None

		# 	получение расширенного датафида (+ хертбит) на основе фильтрованных инструменов
		a = heart.get_heartbeats(dt, tme)
		z=a.copy()
		# 	если мажор укладывается в хертбит считаем медианы через persec секунд
		if medper < persec:
			medper += 1
		else:
			medper = 0
			for key in B:
				if a[B[key][0]]['medheartbeat'] != None and tme - a[B[key][0]]['lasttime'] < a[B[key][0]][
					'medheartbeat']:
					yes = True
					for i in B[key]:
						# сперва проверка на нормальность  всех котиров фьючей с общей базой для кореектной синхронизации медианы
						if a[i]['asks'] == [] or a[i]['bids'] == []:
							yes = False
					# если всё ок
					if yes:
						for i in B[key]:
							Ask = a[i]['asks'][0][0]
							Bid = a[i]['bids'][0][0]
							data = (Ask + Bid) / 2
							mediana = scie.getshlifmed_exp(data, i, medperiod)
							if mediana != None:
								# заполнение корректировочных кэфов по каждому инструменту
								baza[i] = 100 / mediana
		for key in B:
			mascen = []
			for i in B[key]:
				if i in baza:
					# перемножить все цены на кэфы и впаковать в суперстакан доп
					for k in z[i]['asks']:
						z[i]['asks'][k][0]=z[i]['asks'][k][0]*baza[i]
					for k in z[i]['bids']:
						z[i]['bids'][k][0]=z[i]['bids'][k][0]*baza[i]

						                              
					Ask = a[i]['asks'][0][0]
					Bid = a[i]['bids'][0][0]
					data = baza[i] * (Ask + Bid) / 2
					mascen.append((i, data))
			if mascen != []:
				ln = len(mascen)
				sc = 0
				for i in range(ln - 1):
					sc += 1
					mainf = mascen[ln - sc][0]
					b0 = mascen[:ln - sc]
					b = []
					for xo in b0:
						b.append(xo[1])
					bazasred[mainf] = mean(b)
				# print(mainf,"   ",bazasred[mainf])



		for instrument in A:
			# заполним массивы для вывод
			if a[instrument]['medheartbeat']!=None and instrument in bazasred and bazaso[instrument] != None and \
					tme - a[instrument]['lasttime'] < a[instrument]['medheartbeat']:


				Ask = a[instrument]['asks'][0][0] * baza[instrument]
				Bid = a[instrument]['bids'][0][0] * baza[instrument]
				Ask2 = a[instrument]['asks'][0][0]
				Bid2 = a[instrument]['bids'][0][0]

				deals[instrument]["longvh"] = ((bazasred[instrument]- Ask) - Akoefin * (Ask - Bid)) - (comis + forain)
				deals[instrument]["shortvh"] =  ((Bid - bazasred[instrument]) - Akoefin * (Ask - Bid)) - (comis + forain)

				LONG = deals[instrument]["longvh"] < limsig and deals[instrument]["longvh"] > 0
				SHORT = deals[instrument]["shortvh"] < limsig and deals[instrument]["shortvh"] > 0

				if LONG and deals[instrument]["flaglong"]:
					deals[instrument]["lastlong"]= Ask2
					deals[instrument]["flaglong"] =False
					deals[instrument]["flagshort"]=True
					try:
						pr=-comis+100*(deals[instrument]["lastshort"]-deals[instrument]["lastlong"])/ deals[instrument]["lastshort"]
						deals[instrument]["profit"]+= pr
						total += pr
						print(
							f' instrument=  {instrument}    LONG profit =  {deals[instrument]["profit"]}   total {total} ')
					except:
						pass


					# print("LONG   ",Ask2)
				if SHORT and deals[instrument]["flagshort"]:
					deals[instrument]["lastshort"] = Bid2
					deals[instrument]["flagshort"]=False
					deals[instrument]["flaglong"] = True
					try:
						pr=-comis+100*( deals[instrument]["lastshort"]-deals[instrument]["lastlong"]) / deals[instrument]["lastlong"]
						deals[instrument]["profit"] += pr
						total+= pr
						print(
							f'  instrument=  {instrument}  SHORT profit =  {deals[instrument]["profit"] }  total {total}  ')
					except:
						pass




				# print("SHORT  ", Bid2)


			# comisaskmas.append(bazasred[instrument]+comis)
			# comisbidmas.append(bazasred[instrument] - comis)
			#
			# Askotkl=bazasred[instrument]+bazaso[instrument]
			# Bidotkl=bazasred[instrument]-bazaso[instrument]
			# askotklmas.append(Askotkl)
			# bidotklmas.append(Bidotkl)



			# Ask =a[instrument3]['asks'][0][0]*baza[instrument3]
			# Bid =a[instrument3]['bids'][0][0]*baza[instrument3]
			# askmas3.append(Ask)
			# # bidmas3.append(Bid)

			# ixmas.append(x)
	#

	except RuntimeError:
		print("StopIteration error handled successfully")
		break
	except Exception:
		traceback.print_exc()
		print('stop')
		break

# 	выведем эту радость
#
# color = get_color()
# fig = px.line()
#
# # clr = color()
# fig.add_scatter(x=ixmas, y=askmas, line_color=clr, name=' ask')
# fig.add_scatter(x=ixmas, y=bidmas, line_color=clr, name=' bid')
# clr = color()
# fig.add_scatter(x=ixmas, y=bazmas, line_color=clr, name=' baza')
# clr = color()
# fig.add_scatter(x=ixmas, y=askotklmas, line_color=clr, name=' askotk')
# fig.add_scatter(x=ixmas, y=bidotklmas, line_color=clr, name=' bidotk')
# clr = color()
# fig.add_scatter(x=ixmas, y=comisaskmas, line_color=clr, name=' comisask')
# fig.add_scatter(x=ixmas, y=comisbidmas, line_color=clr, name=' comisbid')

# fig = make_subplots(rows=2, cols=1)
#
# color = get_color()
# clr = color()
# fig.add_trace(go.Scatter( x=ixmas,     y=askmas, line_color=clr, name=' ask'), row=1, col=1)
# fig.add_trace(go.Scatter(  x=ixmas, y=bidmas, line_color=clr, name=' bid'), row=1, col=1)
# clr = color()
# fig.add_trace(go.Scatter(  x=ixmas, y=bazmas, line_color=clr, name=' baza'), row=1, col=1)
#
# clr = color()
# fig.add_trace(go.Scatter( x=ixmas,     y=askmas2, line_color=clr, name=' ask'), row=2, col=1)
# fig.add_trace(go.Scatter(  x=ixmas, y=bidmas2, line_color=clr, name=' bid'), row=2, col=1)
#
# clr = color()
# fig.add_trace(go.Scatter( x=xlongmas,     y=ylongmas, line_color=clr, name=' LONG', mode='markers'), row=1, col=1)
# clr = color()
# fig.add_trace(go.Scatter(  x=xshortmas, y=yshortmas, line_color=clr, name=' SHORT', mode='markers'), row=1, col=1)
#
# fig.show()