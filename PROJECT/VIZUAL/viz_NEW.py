from PROJECT.TEST.Test_lib import getdata_merge
from Viz_lib import get_color
from platform import system
import plotly.express as px
import lzma as lz
import json
import time



markets=['binance','whitebit','bybit','huobi','bingx', 'binanceusdm']  #,'MOEX'
minutki=0
onlymerge=0
in_instruments = ['DOGE']
	# [ 'NG-1.23*FRTS',  'NG-2.23*FRTS',  'NG-3.23*FRTS']
not_in_instruments = ['AED']
start_year, start_month, start_day, start_hour = 2024, 1, 1, 1
stop_year, stop_month, stop_day, stop_hour = 	 2024, 1, 7, 10
fixkf=1
getpath = 'G:\\DATA_SBOR\\KRIPTA' if system() == 'Windows' else '/media/roman/J/DATA_SBOR'



stper=60 if minutki else 3600
content = getdata_merge(onlymerge,minutki,markets,getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
print(content)

data = dict()
nomfile=-1
timer2=time.time()
for cont in content:
	a=dict()
	for name in cont:
		# timer=time.time()
		with lz.open(name) as f:
			bb = dict(json.loads(lz.decompress(f.read()).decode('utf-8')))
		# print(f" unpasking time= {time.time() - timer}")
		a |= bb
		inlist = list(a)
		inlist.sort()
		print(len(inlist), "  ", inlist, "  ",name)
		# print(a['Si-9.23*FRTS'])
	# print(a)

	nomfile+=1
	for inst in a:
		for ix in in_instruments:
			for nix in not_in_instruments:
				if ix in inst and nix not in inst:
					if inst not in data:
						data[inst]=dict()
						data[inst]['askmas'] = []
						data[inst]['bidmas'] = []
						data[inst]['ixmas'] =[]
					for tmp in range(stper):
						data[inst]['ixmas'].append(tmp+stper*nomfile)
						if str(tmp) in a[inst]:
							if "kf" not in data[inst]:

								kf = 200 / (a[inst][str(tmp)][0] + a[inst][str(tmp)][1])
								kf = 1 if fixkf == False else kf
								data[inst]['kf']=kf

								data[inst]['lastask'] = a[inst][str(tmp)][0]
								data[inst]['lastbid'] = a[inst][str(tmp)][1]


							data[inst]['askmas'].append(a[inst][str(tmp)][0] * data[inst]['kf'])
							data[inst]['bidmas'].append(a[inst][str(tmp)][1] * data[inst]['kf'])
							data[inst]['lastask'] = a[inst][str(tmp)][0]
							data[inst]['lastbid'] = a[inst][str(tmp)][1]

						else:
							if "kf" in data[inst]:
								data[inst]['askmas'].append(data[inst]['lastask'] * data[inst]['kf'])
								data[inst]['bidmas'].append(data[inst]['lastbid'] * data[inst]['kf'])
							else:
								data[inst]['askmas'].append(None)
								data[inst]['bidmas'].append(None)


# print(f" 2 time= {time.time() - timer2}")
# print(list(data))
color = get_color()
fig = px.line()
for inst in data:
	clr = color()
	fig.add_scatter(x=data[inst]['ixmas'], y=data[inst]['askmas'], line_color=clr, name=inst + ' ask')
	fig.add_scatter(x=data[inst]['ixmas'], y=data[inst]['bidmas'], line_color=clr, name=inst + ' bid')
fig.show()