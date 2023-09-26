from PROJECT.TEST.Test_lib import getdata_merge, gettm
from PROJECT.VIZUAL.Viz_lib import get_color
from platform import system
import plotly.express as px
import lzma as lz
import json
import time

markets = ['FRTS']  # ,'MOEX'
minutki = 0
onlymerge = 0
in_instrument = 'NG-10.23*FRTS'

start_year, start_month, start_day, start_hour = 2023, 9, 21, 14
stop_year, stop_month, stop_day, stop_hour = 2023, 9, 21, 16

getpath = 'G:\\DATA_SBOR' if system() == 'Windows' else '/media/roman/J/DATA_SBOR'

stper = 60 if minutki else 3600
content = getdata_merge(onlymerge, minutki, markets, getpath, start_year, start_month, start_day, start_hour, stop_year,
						stop_month, stop_day, stop_hour)
print(content)


def getd(content):
	for cont in content:
		a = dict()
		for name in cont:
			timer = time.time()
			with lz.open(name) as f:
				bb = dict(json.loads(lz.decompress(f.read()).decode('utf-8')))
			a |= bb
			yield [a,gettm(cont[0])]


def getl2(content):
	z = getd(content)

	L2 = dict()
	while True:
		cc = next(z)
		a=cc[0]
		starttime=cc[1]

		print(len(a))
		# обохначим списки инструментов
		for inst in a:
			if inst not in L2:
				if True:  #inst == 'Eu-12.23*FRTS'
					L2[inst] = dict()
					L2[inst]['asks'] = []
					L2[inst]['bids'] = []
					L2[inst]['time'] = 0
		for ttm in range(3600):
			tmp=str(ttm)
			for inst in a:
				if tmp in a[inst]:
					if True:   #inst == 'Eu-12.23*FRTS'
						L2[inst]['asks'] = a[inst][tmp]['asks']
						L2[inst]['bids'] = a[inst][tmp]['bids']
						L2[inst]['time'] = starttime+ ttm
			yield L2








z=getl2(content)

while True:
	try:
		next(z)
		next(z)
		next(z)
		next(z)
		next(z)
		next(z)
		next(z)
		next(z)
		next(z)
		next(z)
		next(z)
		next(z)
		next(z)
		next(z)
		next(z)
		print(next(z))
		print(next(z))
		print(next(z))
		print(next(z))
		print(next(z))
		break

	except:
		print('stop')
		break


