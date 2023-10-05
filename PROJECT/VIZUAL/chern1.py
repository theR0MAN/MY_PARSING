from PROJECT.TEST.Test_lib import getdata_merge
from Viz_lib import get_color
from platform import system
import plotly.express as px
import lzma as lz
import json
import time

markets = ['FRTS']  # ,'MOEX'
minutki = 0
onlymerge = 0
in_instruments = ['NG-']
# [ 'NG-1.23*FRTS',  'NG-2.23*FRTS',  'NG-3.23*FRTS']
not_in_instruments = ['HANG']
start_year, start_month, start_day, start_hour = 2023, 9, 22, 9
stop_year, stop_month, stop_day, stop_hour = 2023, 9, 22, 9
fixkf = 1
getpath = 'G:\\DATA_SBOR' if system() == 'Windows' else '/media/roman/J/DATA_SBOR'

stper = 60 if minutki else 3600
content = getdata_merge(onlymerge, minutki, markets, getpath, start_year, start_month, start_day, start_hour, stop_year,
						stop_month, stop_day, stop_hour)
print(content)

data = dict()
nomfile = -1
timer2 = time.time()
for cont in content:
	a = dict()
	for name in cont:
		# timer=time.time()
		with lz.open(name) as f:
			bb = dict(json.loads(lz.decompress(f.read()).decode('utf-8')))
		# print(f" unpasking time= {time.time() - timer}")
		a |= bb
		inlist = list(a)
		inlist.sort()
		print(inlist)
