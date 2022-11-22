from MAIN.FUNC import *
import os
import plotly.express as px
import lzma as lz
import json

in_instruments = ['Si-6.22*FRTS', 'Si-9.22*FRTS', 'Si-12.22*FRTS',  'Si-3.23*FRTS']
not_in_instruments = ['@']

if system() == 'Windows':
	getpath = 'G:\\greatOLDHIST\\FORTSALL'
else:
	getpath = '/media/roman/J/greatOLDHIST/FORTSALL'

start_year, start_month, start_day, start_hour = 2022, 4, 7, 10
stop_year, stop_month, stop_day, stop_hour =      2022, 4, 8, 18

content = getdata(getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
print(content)

for name in content:
	with lz.open(name) as f:
		a = dict(json.loads(lz.decompress(f.read()).decode('utf-8')))

	inlist = list(a)
	inlist.sort()
	print(len(inlist), inlist)

	instrs = []
	for inst in a:
		for ix in in_instruments:
			for nix in not_in_instruments:
				if ix in inst and nix not in inst:
					instrs.append(inst)

	print(instrs)
	data = dict()
	first_keys=[]
	for i in instrs:
		first_keys.append(int(next(iter(a[i]))))
	first_key =max(first_keys)
	# first_key = int(next(iter(a[next(iter(a))])))
	for inst in instrs:
		data[inst] = dict()
		kf = 200 / (a[inst][str(first_key)]['a'] + a[inst][str(first_key)]['b'])
		data[inst]['kf'] = kf
		data[inst]['lastask'] = a[inst][str(first_key)]['a']
		data[inst]['lastbid'] = a[inst][str(first_key)]['b']
		data[inst]['asks'] = []
		data[inst]['bids'] = []

	# print(f" inst {inst}  lastask {data[inst]['lastask']}  lastbid {data[inst]['lastbid']}")
	ixes = []
	for i in range(first_key, 3601):
		ixes.append(i)

	for inst in instrs:
		for i in range(first_key, 3601):
			if str(i) in a[inst]:
				data[inst]['asks'].append(a[inst][str(i)]['a'] * data[inst]['kf'])
				data[inst]['bids'].append(a[inst][str(i)]['b'] * data[inst]['kf'])

				data[inst]['lastask'] = a[inst][str(i)]['a']
				data[inst]['lastbid'] = a[inst][str(i)]['b']

			else:
				data[inst]['asks'].append(data[inst]['lastask'] * data[inst]['kf'])
				data[inst]['bids'].append(data[inst]['lastbid'] * data[inst]['kf'])

	color = get_color()
	fig = px.line()
	for inst in data:
		clr = color()
		fig.add_scatter(x=ixes, y=data[inst]['asks'], line_color=clr, name=inst + ' ask')
		fig.add_scatter(x=ixes, y=data[inst]['bids'], line_color=clr, name=inst + ' bid')
	print("SHOW NAME ", name)
	fig.show()

