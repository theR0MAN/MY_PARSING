from PROJECT.TEST.Test_lib import *
from PROJECT.VIZUAL.Viz_lib import get_color
from PROJECT.SCIENTIC.sc_sredn_lib import *
from platform import system
import plotly.express as px
from collections import deque
import datetime, time 		# timer=time.time()
import traceback

markets = ['FRTS']  # ,'MOEX'
minutki = 0
onlymerge = 0
instrument = 'Si-6.24*FRTS'

start_year, start_month, start_day, start_hour = 2023, 9, 20, 12
stop_year, stop_month, stop_day, stop_hour = 2023, 9, 20, 16

getpath = 'G:\\DATA_SBOR' if system() == 'Windows' else '/media/roman/J/DATA_SBOR'
content = getdata_merge(onlymerge, minutki, markets, getpath, start_year, start_month, start_day, start_hour, stop_year,
						stop_month, stop_day, stop_hour)
print(content)

askmas = []
bidmas = []
srexpmas = []
sreasymas = []
medmas = []
shlifmedmas = []
shlifmedmas2 = []
shlifmedmas20 = []
ixmas = []
tm = 0
# z = get_l2(content)

heart=Myheartbeat(100,50,0.8,2)
exem = Getl2(content)
z = exem.get_l2()  # получает словарь котиров
while True:
	try:
		dt = next(z)
		tme=exem.ttime
		a=heart.get_heartbeats(dt,tme)
		print(a[instrument ]['medheartbeat'])

		# print(tme)
		# for key in dt:
		# 	if key not  in a:
		# 		a[key] =dict()
		# 		a[key]['asks'] =dt[key]['asks']
		# 		a[key]['bids'] = dt[key]['bids']
		# 		a[key]['time'] = tme
		# 		a[key]['kvotimestamps'] = 0
		# 		a[key]['kvoraschet'] =0
		# 		a[key]['heartbeat'] = deque()
		# 		a[key]['medheartbeat'] = None
		# 	if a[key] ['asks'] != dt[key] ['asks'] or a[key] ['bids'] != dt[key] ['bids'] :
		# 		a[key]['asks'] = dt[key]['asks']
		# 		a[key]['bids'] = dt[key]['bids']
		# 		a[key]['timestamp'] = tme-a[key]['time']
		# 		a[key]['time'] = tme
		# 		if a[key]['kvotimestamps']< periodhertbeat:
		# 			a[key]['heartbeat'].append(a[key]['timestamp'] )
		# 			a[key]['kvotimestamps'] += 1
		# 			a[key]['kvoraschet'] += 1
		# 		else:
		# 			a[key]['heartbeat'].append(a[key]['timestamp'])
		# 			a[key]['heartbeat'] .popleft()
		# 			a[key]['kvoraschet'] += 1
		# 			if a[key]['kvoraschet']> periodraschet:
		# 				a[key]['kvoraschet'] = 0
		# 				l=list(a[key]['heartbeat'])
		# 				l.sort()
		# 				ln=int(periodhertbeat*part)
		# 				a[key]['medheartbeat'] =l[ln]*mnoz
						# if key == instrument:
						# 	print(l,'      ',a[key]['medheartbeat'])


	except RuntimeError:
		print("StopIteration error handled successfully")
		break
# except Exception:
# 	traceback.print_exc()
# 	print('stop')
# 	break
#

