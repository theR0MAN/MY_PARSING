from G_FUNC import *
from platform import system
import plotly.express as px

import json
import time




markets=['MOEX','FRTS',]
minutki=1
onlymerge=0
in_instruments = ['SBER','SBRF-6.23']
	# [ 'NG-1.23*FRTS',  'NG-2.23*FRTS',  'NG-3.23*FRTS']
not_in_instruments = ['HANG']
start_year, start_month, start_day, start_hour = 2023, 5, 23, 12
stop_year, stop_month, stop_day, stop_hour = 	 2023, 5, 23, 12
fixkf=1
getpath = 'G:\\DATA_SBOR' if system() == 'Windows' else '/media/roman/J/DATA_SBOR'



stper=60 if minutki else 3600
content = getdata_merge(onlymerge,minutki,markets,getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
print(content)

data = dict()
nomfile=-1
for cont in content:
	a=get_dict(cont)



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
								try:
									kf = 200 / (a[inst][str(tmp)]['asks'][0][0] + a[inst][str(tmp)]['bids'][0][0])
								except:
									kf = 200 / (a[inst][str(tmp)]['a'] + a[inst][str(tmp)]['b'])
								kf = 1 if fixkf == False else kf
								data[inst]['kf']=kf
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


# корректировка и синхронизация


ixes=[]
delset= set()
k=0
for inst in data:
	k = len(data[inst]['askmas'])
	print(k)
	break
for inst in data:
	for i in range (k):
		if data[inst]['askmas'][i] == None :
			delset.add(i)


inst1= list(data)[0]
inst2=list(data)[1]


# k1= list(data[0])
# print(' opaopa ',k1)
data2={}
data2['spread'] = {}
data2['spread']['ask'] = []
data2['spread']['bid'] = []
for inst in data:
	data2[inst] = {}
	data2[inst]['askmas'] = []
	data2[inst]['bidmas'] = []
cty=0
for i in range (k):
	if i not in delset:
		ixes.append(cty)
		cty = cty + 1
		for inst in data:
			data2[inst]['askmas'].append(data[inst]['askmas'][i])
			data2[inst]['bidmas'].append(data[inst]['bidmas'][i])


for i in range (cty-1):
	data2['spread']['ask'].append(data2[inst1]['askmas'][i] - data2[inst2]['bidmas'][i]+100)
	data2['spread']['bid'].append( data2[inst1]['bidmas'][i] -data2[inst2]['askmas'][i]+100)




color = get_color()
fig = px.line()
clr = color()
fig.add_scatter(x=ixes, y=data2[inst1]['askmas'], line_color=clr, name=inst1 + ' ask')
fig.add_scatter(x=ixes, y=data2[inst1]['bidmas'], line_color=clr, name=inst1 + ' bid')
clr = color()
fig.add_scatter(x=ixes, y=data2[inst2]['askmas'], line_color=clr, name=inst2 + ' ask')
fig.add_scatter(x=ixes, y=data2[inst2]['bidmas'], line_color=clr, name=inst2 + ' bid')
clr = color()
fig.add_scatter(x=ixes, y=data2['spread']['ask'], line_color=clr, name=' ask')
fig.add_scatter(x=ixes, y=data2['spread']['bid'], line_color=clr, name=' bid')

fig.show()

# color = get_color()
# fig = px.line()
# clr = color()
# fig.add_scatter(x=ixes, y=data2['spread']['ask']+100, line_color=clr, name=' ask')
# fig.add_scatter(x=ixes, y=data2['spread']['bid']+100, line_color=clr, name=' bid')
# fig.show()
