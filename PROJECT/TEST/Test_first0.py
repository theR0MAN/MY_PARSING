from PROJECT.TEST.Test_lib import *
from PROJECT.VIZUAL.Viz_lib import get_color
from platform import system
import plotly.express as px
import time

markets = ['FRTS']  # ,'MOEX'
minutki = 0
onlymerge = 0
instrument = 'Eu-12.23*FRTS'

start_year, start_month, start_day, start_hour = 2023, 9, 20, 14
stop_year, stop_month, stop_day, stop_hour = 2023, 9, 20, 14

getpath = 'G:\\DATA_SBOR' if system() == 'Windows' else '/media/roman/J/DATA_SBOR'
content = getdata_merge(onlymerge, minutki, markets, getpath, start_year, start_month, start_day, start_hour, stop_year,
						stop_month, stop_day, stop_hour)
print(content)


askmas = []
bidmas = []
ixmas = []
tm = 0
z = get_l2(content)

# exem = Getl2(content)
# z = exem.get_l2()
while True:
	try:
		a = next(z)
		# print(exem.output)
		if a[instrument]['time'] !=0:
			askmas.append(a[instrument]['asks'][0][0])
			bidmas.append(a[instrument]['bids'][0][0])
			ixmas.append(tm)
			tm += 1

	except:
		print('stop')
		break

color = get_color()
clr = color()
fig = px.line()
fig.add_scatter(x=ixmas, y=askmas, line_color=clr, name= ' ask')
fig.add_scatter(x=ixmas, y=bidmas, line_color=clr, name=' bid')
bidmas2=[]
ixmas2=[]
for i in range(0, len(ixmas), 30):
	ixmas2.append(i)
	bidmas2.append(bidmas[i])
fig.add_scatter(x=ixmas2, y=bidmas2, line_color='red', mode='markers', name=' M')

fig.show()
# переделать саисок брать из даты раз в день.
# Для даты- время записывать только раз, а не для каждого котира. При отсутствии котиров -НОН, а не 0 в дате
# исследовать хеартбиты

