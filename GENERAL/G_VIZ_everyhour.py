from G_FUNC import *
import os
import plotly.express as px
import lzma as lz
import json
import time


in_instruments = ['Si-12.22*FRTS', 'Si-3.23*FRTS', 'Si-6.23*FRTS']
not_in_instruments = ['VTB']
start_year, start_month, start_day, start_hour = 2022, 11, 25, 8
stop_year, stop_month, stop_day, stop_hour = 	 2022, 11, 25, 8
fixkf = True


if system() == 'Windows':
	getpath = 'G:\\DATA_SBOR\\FRTS\\'
else:
	getpath = '/media/roman/J/greatOLDHIST/FORTSALL'


def find_key(dct, key):
	if key in dct:
		return key
	else:
		for i in range(int(key) - 1, -1, -1):
			if str(i) in dct:
				return str(i)


content = getdata(getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour,
				  '.roman')
print(content)

first = True
for name in content:
	with lz.open(name) as f:
		a = dict(json.loads(lz.decompress(f.read()).decode('utf-8')))

	instrs = []
	for inst in a:
		for ix in in_instruments:
			for nix in not_in_instruments:
				if ix in inst and nix not in inst:
					instrs.append(inst)
	if first:
		first = False
		inlist = list(a)
		inlist.sort()
		print(len(inlist), inlist)
		print(instrs)

	data = dict()
	first_keys = []
	for inst in instrs:
		first_keys.append(int(next(iter(a[inst]))))
	first_key = str(max(first_keys))

	flagbreak = False
	for inst in instrs:
		data[inst] = dict()
		fndkey = find_key(a[inst], first_key)
		if fndkey == None:
			zz = list(a[inst])
			print(f" break {inst} {name}  first_key={first_key}  {zz} ")
			flagbreak = True
			break
		try:
			kf = 200 / (a[inst][fndkey]['asks'][0][0] + a[inst][fndkey]['bids'][0][0])
		except:
			kf = 200 / (a[inst][fndkey]['a'] + a[inst][fndkey]['b'])
		kf = 1 if fixkf == False else kf

		data[inst]['kf'] = kf
		try:
			data[inst]['lastask'] = a[inst][fndkey]['asks'][0][0]
			data[inst]['lastbid'] = a[inst][fndkey]['bids'][0][0]
		except:
			data[inst]['lastask'] = a[inst][fndkey]['a']
			data[inst]['lastbid'] = a[inst][fndkey]['b']

		data[inst]['askmas'] = []
		data[inst]['bidmas'] = []

	if flagbreak:
		continue
	else:
		ixes = []
		for i in range(int(first_key), 3601):
			ixes.append(i)

		for inst in instrs:
			for i in range(int(first_key), 3601):
				if str(i) in a[inst]:
					try:
						data[inst]['askmas'].append(a[inst][str(i)]['asks'][0][0] * data[inst]['kf'])
						data[inst]['bidmas'].append(a[inst][str(i)]['bids'][0][0] * data[inst]['kf'])
						data[inst]['lastask'] = a[inst][str(i)]['asks'][0][0]
						data[inst]['lastbid'] = a[inst][str(i)]['bids'][0][0]
					except:
						data[inst]['askmas'].append(a[inst][str(i)]['a'] * data[inst]['kf'])
						data[inst]['bidmas'].append(a[inst][str(i)]['b'] * data[inst]['kf'])
						data[inst]['lastask'] = a[inst][str(i)]['a']
						data[inst]['lastbid'] = a[inst][str(i)]['b']


				else:
					data[inst]['askmas'].append(data[inst]['lastask'] * data[inst]['kf'])
					data[inst]['bidmas'].append(data[inst]['lastbid'] * data[inst]['kf'])

		color = get_color()
		fig = px.line()
		for inst in data:
			clr = color()
			fig.add_scatter(x=ixes, y=data[inst]['askmas'], line_color=clr, name=inst + ' ask')
			fig.add_scatter(x=ixes, y=data[inst]['bidmas'], line_color=clr, name=inst + ' bid')
		print("SHOW NAME ", name)
		fig.show()
