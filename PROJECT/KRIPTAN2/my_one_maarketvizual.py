from PROJECT.TEST.Test_lib import *
from PROJECT.VIZUAL.Viz_lib import get_color
from PROJECT.SCIENTIC.sc_sredn_lib import *
from platform import system
import plotly.express as px
from collections import deque
import datetime, time  # timer=time.time()
import traceback
import statistics
zadpol=3
zadtmsmp=3

pth='G:\\NEWKRIPT'

# markets = os.listdir(pth)
markets = ['bybit&swap', ]  #'poloniex',24 1  7-10
print(markets)

# markets = ['FRTS2']  # ,'MOEX'
instdict = dict()

minutki = 123
onlymerge = 0

start_year, start_month, start_day, start_hour = 2024, 3, 20, 2
stop_year, stop_month, stop_day, stop_hour = 2024, 3, 20, 2

content = getdata_merge(onlymerge, minutki, markets, pth, start_year, start_month, start_day, start_hour, stop_year,
						stop_month, stop_day, stop_hour)
print(content)

if content==[]:
	print(' нет данных за этот период' )
	quit()

exem = Getl2(content, 200, 0.95, 10)
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

data = next(z)
# готовим итоговый массив
rezdict = dict()
for sym in data:
	rezdict[sym] = dict()
	rezdict[sym]['asks'] = []
	rezdict[sym]['bids'] = []

while True:

	try:
		# timer=time.time()
		data = next(z)  # это якобы на серваке - к нему нужен доступ


		timestamps=[]
		medtmamp =0
		for inst in data:
			if data[inst]['dat'] != None:
				tmst=data[inst]['dat']['timestamp']
				timestamps.append(tmst)
		if timestamps!=[]:
			medtmamp=statistics.median(timestamps)


		for inst in data:
			# print(instr, inst,data [inst]['dat'])
			if data [inst]['dat'] != None:
				# print(f" { inst} timestamp={data [inst]['dat']['timestamp']}  {medtmamp-data [inst]['dat']['timestamp']}   ")
				if data [inst]['tmstp'][1]<zadpol and medtmamp-data [inst]['dat']['timestamp']<zadtmsmp:
					rezdict  [inst]['asks'].append (data [inst]['dat']['asks'][0])
					rezdict  [inst]['bids'].append(data [inst]['dat']['bids'][0])
				else:
					# if data [inst]['tmstp'][1] > zadpol:
					# 	print('zaderzka zadpol', inst)
					# if medtmamp-data [inst]['dat']['timestamp']<zadtmsmp:
					# 	print('zaderzka zadtmsmp',  inst)


					rezdict  [inst]['asks'].append(None)
					rezdict  [inst]['bids'].append(None)
			else:
				rezdict  [inst]['asks'].append(None)
				rezdict  [inst]['bids'].append(None)


		ixes.append(count)
		count += 1

	except Exception:
		print(traceback.format_exc())
		print('error')
		# quit()
		break
# нормализация словаря
delspis=[]
for instr in rezdict:
	for  inst in rezdict :
		sm=0
		cnt=0
		ind=-1
		for ask in rezdict  [inst]['asks']:
			ind+=1
			if ask != None :
				bid=rezdict  [inst]['bids'][ind]
				sm+=(ask+bid)/2
				cnt+=1
		if cnt !=0:
			sredn =sm/cnt
			ind = -1
			for ask in rezdict  [inst]['asks']:
				ind += 1
				if ask != None:
					rezdict  [inst]['bids'][ind]=100*rezdict  [inst]['bids'][ind]/ sredn
					rezdict  [inst]['asks'][ind] = 100 * rezdict  [inst]['asks'][ind] / sredn

		else:
			delspis.append(inst)
			# print( 'None data', inst)

print(delspis)
# quit()
# чистка полностью отсутствующих данных
for  inst in delspis:
	del rezdict [inst]
	print('None data - удаление ',  inst)



print(  'вывод оставшихся графиков' )
# for sym in rezdict:
# 	print(sym, len(rezdict[sym]),rezdict[sym])
# quit()
# firstkey= next(iter(rezdict))
# ln=len(rezdict[firstkey]['asks'])
# print(ln)
# quit()

color = get_color()
fig = px.line()
for  inst in rezdict:
	clr = color()
	fig.add_scatter(x=ixes, y=rezdict [inst]['asks'], line_color=clr, name= inst + ' ask')
	fig.add_scatter(x=ixes, y=rezdict[inst]['bids'], line_color=clr, name= inst+ ' bid')
fig.show()