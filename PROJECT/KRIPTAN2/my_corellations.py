from PROJECT.TEST.Test_lib import *
from PROJECT.VIZUAL.Viz_lib import get_color
from PROJECT.SCIENTIC.sc_sredn_lib import *
from platform import system
import plotly.express as px
from collections import deque
import datetime, time  # timer=time.time()
import traceback
import statistics
import pandas as pd
from PROJECT.SBOR.my_lib import *
# from IPython.display import display

zadpol=3
zadtmsmp=2

pth='G:\\NEWKRIPT'

# markets = os.listdir(pth)
markets = ['bybit&swap', ]  #'poloniex',24 1  7-10
print(markets)

# markets = ['FRTS2']  # ,'MOEX'
instdict = dict()

minutki = 123
onlymerge = 0

start_year, start_month, start_day, start_hour = 2024, 3, 18, 10
stop_year, stop_month, stop_day, stop_hour = 2024, 3, 18, 16

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
cordat = dict()
for sym in data:
	cordat[sym]=[]
	rezdict[sym] = dict()
	rezdict[sym]['asks'] = []
	rezdict[sym]['bids'] = []
kcnt=0
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


		wrt=True
		for inst in data:
			if data [inst]['dat'] != None:
				if not (data [inst]['tmstp'][1]<zadpol and medtmamp-data [inst]['dat']['timestamp']<zadtmsmp):
					wrt = False
			else:
				wrt= False

		if wrt:
			for inst in data:
				rezdict[inst]['asks'].append(data[inst]['dat']['asks'][0])
				rezdict[inst]['bids'].append(data[inst]['dat']['bids'][0])
				cordat[inst].append((data[inst]['dat']['asks'][0]+data[inst]['dat']['bids'][0])/2)


			ixes.append(count)
			count += 1

	except Exception:
		print(traceback.format_exc())
		print('error')
		# quit()
		break

# нормализация словаря

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
					cordat[inst][ind]=((rezdict[inst]['bids'][ind] + rezdict[inst]['asks'][ind])/2)


# распилим на снапшоты
ixes2=[]
cordat2=dict()

firstkey= next(iter(cordat))
ln=len(cordat[firstkey])

for inst in cordat:
	cordat2[inst]=cordat[inst][0:ln:10]

firstkey= next(iter(cordat2))
ln=len(cordat2[firstkey])
for i in range(ln):
	ixes2.append(i)

timer=time.time()
kolonki=list(cordat2)
# print(kolonki)
df = pd.DataFrame(cordat2, columns=kolonki)
z= df.corr()
print('skorost = ',time.time()-timer)
print(z)
a=z.to_dict()

for key in a:
	print(key,mysortdict(a[key]))
# quit()
# z.to_csv("output.csv",sep=';', index=False)


color = get_color()
fig = px.line()
for  inst in rezdict:
	clr = color()
	fig.add_scatter(x=ixes, y=rezdict [inst]['asks'], line_color=clr, name= inst + ' ask')
	fig.add_scatter(x=ixes, y=rezdict[inst]['bids'], line_color=clr, name= inst+ ' bid')
fig.show()


color = get_color()
fig = px.line()
for  inst in cordat2:
	clr = color()
	fig.add_scatter(x=ixes2, y=cordat2 [inst], line_color=clr, name= inst + ' ask')
#
fig.show()