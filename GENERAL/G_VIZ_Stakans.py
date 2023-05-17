from G_FUNC import *
from platform import system
import plotly.express as px
import lzma as lz
import json
import time

markets = ['FRTS']

in_instruments = ['NG-1.23*FRTS', 'NG-3.23*FRTS']  # ,'NG-3.23*FRTS'
not_in_instruments = ['HANG']
start_year, start_month, start_day, start_hour = 2023, 1, 5, 14
fixkf = True
getpath = 'G:\\DATA_SBOR' if system() == 'Windows' else '/media/roman/J/DATA_SBOR'

stper =  3600
content = getdata_merge(0, 0, markets, getpath, start_year, start_month, start_day, start_hour,
						start_year,
						start_month, start_day, start_hour)
print(content)

a = dict()
for cont in content:
	for name in cont:
		timer = time.time()
		with lz.open(name) as f:
			bb = dict(json.loads(lz.decompress(f.read()).decode('utf-8')))
		# print(f" unpasking time= {time.time() - timer}")
		a |= bb
inlist = list(a)
inlist.sort()
print(len(inlist), "  ", inlist)

if len(in_instruments) > 1:
	if in_instruments[0] in a and in_instruments[1] in a:
		print(in_instruments[0])
		print(in_instruments[1])
		viz_stakan2(a[in_instruments[0]], a[in_instruments[1]])

if len(in_instruments) == 1:
	if in_instruments[0] in a:
		print(in_instruments[0])
		viz_stakan1(a[in_instruments[0]])
