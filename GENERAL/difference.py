from G_FUNC import *
from platform import system
import plotly.express as px
import lzma as lz
import json
import time
from operator import sub

markets = ['FRTS']
minutki = 1
onlymerge = 0
in_instruments = ['GAZR-6.23*FRTS', 'GAZR-9.23*FRTS']
# [ 'NG-1.23*FRTS',  'NG-2.23*FRTS',  'NG-3.23*FRTS']
not_in_instruments = ['HANG']
start_year, start_month, start_day, start_hour = 2023, 5, 15, 0
stop_year, stop_month, stop_day, stop_hour =     2023, 5, 17, 20
fixkf = 1
getpath = 'G:\\DATA_SBOR' if system() == 'Windows' else '/media/roman/J/DATA_SBOR'

stper = 60 if minutki else 3600
content = getdata_merge(onlymerge, minutki, markets, getpath, start_year, start_month, start_day, start_hour, stop_year,
						stop_month, stop_day, stop_hour)
print(content)

data = dict()
nomfile = -1
for cont in content:
	a = dict()
	for name in cont:
		timer = time.time()
		with lz.open(name) as f:
			bb = dict(json.loads(lz.decompress(f.read()).decode('utf-8')))
		print(f" unpasking time= {time.time() - timer}")
		a |= bb
		inlist = list(a)
		inlist.sort()
		print(len(inlist), "  ", inlist, "  ", name)

	nomfile += 1
	for inst in a:
		for ix in in_instruments:
			for nix in not_in_instruments:
				if ix in inst and nix not in inst:
					if inst not in data:
						data[inst] = dict()
						data[inst]['askmas'] = []
						data[inst]['bidmas'] = []
						data[inst]['ixmas'] = []
					for tmp in range(stper):

						data[inst]['ixmas'].append(tmp + stper * nomfile)
						if str(tmp) in a[inst]:
							if "kf" not in data[inst]:
								try:
									kf = 200 / (a[inst][str(tmp)]['asks'][0][0] + a[inst][str(tmp)]['bids'][0][0])
								except:
									kf = 200 / (a[inst][str(tmp)]['a'] + a[inst][str(tmp)]['b'])
								kf = 1 if fixkf == False else kf
								data[inst]['kf'] = kf
								try:
									data[inst]['lastask'] = a[inst][str(tmp)]['asks'][0][0]
									data[inst]['lastbid'] = a[inst][str(tmp)]['bids'][0][0]
								except:
									data[inst]['lastask'] = a[inst][str(tmp)]['a']
									data[inst]['lastbid'] = a[inst][str(tmp)]['b']

							try:
								data[inst]['askmas'].append(a[inst][str(tmp)]['asks'][0][0] * data[inst]['kf'])
								data[inst]['bidmas'].append(a[inst][str(tmp)]['bids'][0][0] * data[inst]['kf'])
								data[inst]['lastask'] = a[inst][str(tmp)]['asks'][0][0]
								data[inst]['lastbid'] = a[inst][str(tmp)]['bids'][0][0]
							except:
								data[inst]['askmas'].append(a[inst][str(tmp)]['a'] * data[inst]['kf'])
								data[inst]['bidmas'].append(a[inst][str(tmp)]['b'] * data[inst]['kf'])
								data[inst]['lastask'] = a[inst][str(tmp)]['a']
								data[inst]['lastbid'] = a[inst][str(tmp)]['b']

						else:
							if "kf" in data[inst]:
								data[inst]['askmas'].append(data[inst]['lastask'] * data[inst]['kf'])
								data[inst]['bidmas'].append(data[inst]['lastbid'] * data[inst]['kf'])
							else:
								data[inst]['askmas'].append(None)
								data[inst]['bidmas'].append(None)

print(list(data))
Z=list(data)
print(Z[0])
print(Z[1])

color = get_color()
fig = px.line()

# print(data[Z[0]]['askmas'])
# print(data[Z[1]]['askmas'])
# print(data[Z[0]]['bidmas'])
# print(data[Z[1]]['bidmas'])
clr = color()
fig.add_scatter(x=data[Z[0]]['ixmas'][1:], y=list(map(sub, data[Z[0]]['askmas'][1:], data[Z[1]]['bidmas'][1:])), line_color=clr, name=Z[0] + ' ask')
fig.add_scatter(x=data[Z[0]]['ixmas'][1:], y=list(map(sub, data[Z[0]]['bidmas'][1:], data[Z[1]]['askmas'][1:])), line_color=clr, name=Z[0] + ' bid')
fig.show()

