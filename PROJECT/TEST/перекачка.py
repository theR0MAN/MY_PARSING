# качнем нужные символы

from PROJECT.TEST.Test_lib import getdata_merge
# from Viz_lib import get_color
from platform import system
import plotly.express as px
import lzma as lz
import json
import time



# markets=['MOEX2', 'FRTS2', 'CURcross', 'USAFUT', 'CUR', 'RAW', 'FxMETBR', 'FxCUR']  #,'MOEX'
markets=[ 'CURcross']
minutki=1
onlymerge=0

start_year, start_month, start_day, start_hour = 2024, 1, 10, 12
stop_year, stop_month, stop_day, stop_hour = 	 2024, 1, 10, 12

getpath = 'G:\\DATA_SBOR' if system() == 'Windows' else '/media/roman/J/DATA_SBOR'


content = getdata_merge(onlymerge,minutki,markets,getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
print(content)

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
	print(len(inlist), "  ", inlist)

	for key in a:
		print(key,a[key])