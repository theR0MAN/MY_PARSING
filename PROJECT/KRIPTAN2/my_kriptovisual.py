from PROJECT.TEST.Test_lib import *
from PROJECT.VIZUAL.Viz_lib import get_color
from PROJECT.SCIENTIC.sc_sredn_lib import *
from platform import system
import plotly.express as px
from collections import deque
import datetime, time  # timer=time.time()
import traceback
import statistics
# zadpol=3
zadtmsmp=3

pth='G:\\NEWKRIPT'

have = os.listdir(pth)
print('has dir',have)
quit()
markets = ['bybit&swap','huobi&swap',  'okx&swap','binance&swap', 'bitget&swap']  #'poloniex',24 1  7-10
print(markets)

# markets = ['FRTS2']  # ,'MOEX'
instdict = dict()

minutki = 123
onlymerge = 0

start_year, start_month, start_day, start_hour = 2024, 3, 20, 1
stop_year, stop_month, stop_day, stop_hour = 2024, 3, 20, 2

content = getdata_merge(onlymerge, minutki, markets, pth, start_year, start_month, start_day, start_hour, stop_year,
						stop_month, stop_day, stop_hour)
print(content)

if content==[]:
	print(' нет данных за этот период' )
	quit()

exem = Getl2(content, 200, 0.95,10)
# scie = Mysredn()
z = exem.get_l2NEW()  # получает словарь котиров
day0 = -1
count = 0
ct = 0

razrez = 0
countrr = 0

obryv = dict()
paintdict = {}
# подготовка словаря отрисовки
ixes = []


first=False
instset=set()

limgraf=5 # минимум графиков в окне
while True:

	try:
		# timer=time.time()
		data = next(z)  # это якобы на серваке - к нему нужен доступ

		# print(time.time()-timer)
		tme = exem.ttime  # Эмуляция получения времени
		day = exem.day
		# tms=exem.ttime
		#  эмуляция получения списка инструментов  раз в день
		# if day != day0:
		# 	day0 = day
		# 	year = exem.year
		# 	month = exem.mon

		if not first:
			first=True
			for instfull in data:
				instr=instfull.split('*')[0]
				if ":" in instr:
					instr = instr.split(':')[0]
				instset.add(instr)

			instdict=dict()
			for instr in instset:
				instdict[instr]=[]

			for instfull in data:
				instr=instfull.split('*')[0]
				if ":" in instr:
					instr = instr.split(':')[0]
				instdict[instr].append(instfull)

			spisdel=[]
			for sym in instdict:
				if len(instdict[sym])<limgraf:
					spisdel.append([sym,len(instdict[sym])])


			for dl in spisdel:
				print(" удаление ", dl[0], " в наличии только ", dl[1])
				del instdict[dl[0]]


			# готовим итоговый массив
			rezdict = dict()
			for sym in instdict:
				rezdict[sym] = dict()
				for instful in instdict[sym] :
					rezdict[sym][instful]=dict()
					# rezdict[sym][instful]['koef'] = False
					rezdict[sym][instful]['asks']=[]
					rezdict[sym][instful]['bids'] = []

			# проверка
			print(" количество графиков ", len(rezdict))
			for sym in rezdict:
				print(sym, len(rezdict[sym]),rezdict[sym])

		# for key in data:
		# 	print(key,data[key])
		# LDO / USDT * whitebit  #  {'dat': [3.1223, 3.1174, None, 1.1496474742889404], 'tmstp': [None, 0, False]}
		# quit()
	# 	заполнение
	# 	print(instdict)
	# 	quit()
		timestamps = []
		medtmamp = 0
		for inst in data:
			if data[inst]['dat'] != None:
				tmst = data[inst]['dat']['timestamp']
				timestamps.append(tmst)
		if timestamps != []:
			medtmamp = statistics.median(timestamps)


		for instfull in data:
			instr = instfull.split('*')[0]
			if ":" in instr:
				instr = instr.split(':')[0]
			if instr in rezdict:
				# print(instr,instfull,data[instfull]['dat'])
				if data[instfull]['dat'] != None:
					# print(f" {instfull} timestamp={data[instfull]['dat']['timestamp']}  {medtmamp-data[instfull]['dat']['timestamp']}   ")
					if data[instfull]['tmstp'][2] and medtmamp-data[instfull]['dat']['timestamp']<zadtmsmp:
						rezdict[instr][instfull]['asks'].append (data[instfull]['dat']['asks'][0])
						rezdict[instr][instfull]['bids'].append(data[instfull]['dat']['bids'][0])
					else:
						# if data[instfull]['tmstp'][2] :
						# 	print('zaderzka zadpol',instfull)
						# if medtmamp-data[instfull]['dat']['timestamp']<zadtmsmp:
						# 	print('zaderzka zadtmsmp', instfull)


						rezdict[instr][instfull]['asks'].append(None)
						rezdict[instr][instfull]['bids'].append(None)
				else:
					rezdict[instr][instfull]['asks'].append(None)
					rezdict[instr][instfull]['bids'].append(None)


		ixes.append(count)
		count += 1
		# if count>20:
		# 	for sym in rezdict:
		# 		print(sym, len(rezdict[sym]),rezdict[sym])
		# 	quit()
	except Exception:
		print(traceback.format_exc())
		print('error')
		# quit()
		break

# quit()
# нормализация словаря
delspis=[]
for instr in rezdict:
	for instfull in rezdict[instr]:
		sm=0
		cnt=0
		ind=-1
		for ask in rezdict[instr][instfull]['asks']:
			ind+=1
			if ask != None :
				bid=rezdict[instr][instfull]['bids'][ind]
				sm+=(ask+bid)/2
				cnt+=1
		if cnt !=0:
			sredn =sm/cnt
			ind = -1
			# rezdict[instr][instfull]['koef'] = True
			for ask in rezdict[instr][instfull]['asks']:
				ind += 1
				if ask != None:
					rezdict[instr][instfull]['bids'][ind]=100*rezdict[instr][instfull]['bids'][ind]/ sredn
					rezdict[instr][instfull]['asks'][ind] = 100 * rezdict[instr][instfull]['asks'][ind] / sredn

		else:
			delspis.append(instfull)
			# print( 'None data',instfull)

# чистка полностью отсутствующих данных
for instfull in delspis:
	instr=instfull.split('*')[0]
	if ":" in instr:
		instr = instr.split(':')[0]
	del rezdict[instr][instfull]
	print('None data - удаление ', instfull)

# чистка повторная по количеству инструментов
spisdel = []
for sym in rezdict:
	if len(rezdict[sym]) < limgraf:
		spisdel.append([sym, len(rezdict[sym])])


for dl in spisdel:
	print(" удаление после чистки данных", dl[0], " в наличии только ", dl[1])
	del rezdict[dl[0]]

print(  'вывод оставшихся графиков' )
# for sym in rezdict:
# 	print(sym, len(rezdict[sym]),rezdict[sym])
# quit()
for inst in rezdict:
	color = get_color()
	fig = px.line()
	for instfull in rezdict[inst]:
		clr = color()
		fig.add_scatter(x=ixes, y=rezdict[inst][instfull]['asks'], line_color=clr, name=instfull + ' ask')
		fig.add_scatter(x=ixes, y=rezdict[inst][instfull]['bids'], line_color=clr, name=instfull+ ' bid')
	fig.show()