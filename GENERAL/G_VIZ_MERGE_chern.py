from G_FUNC import *
from platform import system
import plotly.express as px
import lzma as lz
import json




markets=['FRTS']
minutki=0
onlymerge=0
in_instruments = [ 'Si-12.22*FRTS','Si-3.23*FRTS'  ]
not_in_instruments = ['HANG']
start_year, start_month, start_day, start_hour = 2022, 11, 30, 16
stop_year, stop_month, stop_day, stop_hour = 	 2022, 11, 30, 19
fixkf=True
getpath = 'G:\\DATA_SBOR' if system() == 'Windows' else '/media/roman/J/DATA_SBOR'

def find_key(dct, key):
	if key in dct:
		return key
	else:
		for i in range(int(key) - 1, -1, -1):
			if str(kk) in dct:
				return str(kk)



stper=60 if minutki else 3600
content = getdata_merge(onlymerge,minutki,markets,getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
print(content)
# quit()
ixes = []
kk=0
data = dict()
first_key=0
first=True
for cont in content:
	a=dict()
	for name in cont:
		with lz.open(name) as f:
			bb = dict(json.loads(lz.decompress(f.read()).decode('utf-8')))
			a |= bb

	if first:
		first=False
		inlist = list(a)
		inlist.sort()
		print(len(inlist), inlist)

		instrs = []
		for inst in a:
			for ix in in_instruments:
				for nix in not_in_instruments:
					if ix in inst and nix not in inst:
						instrs.append(inst)
		print(len(instrs),"  ",instrs)
		if len(instrs) == 0:
			first = True
			continue

		first_keys = []
		for inst in instrs:
			first_keys.append(int(next(iter(a[inst]))))
		first_key = max(first_keys)

		flagbreak = False
		for inst in instrs:
			data[inst] = dict()
			fndkey = find_key(a[inst], str(first_key))
			if fndkey == None:
				zz=list(a[inst])
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

	if not first:
		first_keys = []
		# for inst in instrs:
		# 	first_keys.append(int(next(iter(a[inst]))))
		# first_key = max(first_keys)
		for inst in instrs:
			for i in range(first_key, stper):
				if str(i) in a[inst]:
					kk+=1
					ixes.append(kk)
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
fig.show()