from PROJECT.TEST.Test_lib import *
from PROJECT.VIZUAL.Viz_lib import get_color
from PROJECT.SCIENTIC.sc_sredn_lib import *
from platform import system
import plotly.express as px
from collections import deque
import datetime, time  # timer=time.time()
import traceback
from statistics import mean
from PROJECT.SBOR.my_lib  import *
from get_my_insts import get_fut
# mysyms = {'GD', 'SV', 'BR', 'NG', 'W4', 'Eu', 'Si', 'MX','ED','SR','SP'}
myklaster=['MAIN','NEAR','USAFUT']
mysyms = ['BR', 'NG']

markets=['MOEX2', 'FRTS2', 'CURcross', 'USAFUT', 'CUR', 'RAW', 'FxMETBR', 'FxCUR']
# markets = ['FRTS2']  # ,'MOEX'
# paintdict={}
instdict=dict()

minutki = 0
onlymerge = 0




start_year, start_month, start_day, start_hour = 2024, 1, 11, 12
stop_year, stop_month, stop_day, stop_hour = 	 2024, 1, 11, 12

content = getdata_merge(onlymerge, minutki, markets, 'G:\\DATA_SBOR', start_year, start_month, start_day, start_hour, stop_year,
						stop_month, stop_day, stop_hour)
print(content)


exem = Getl2(content)
# scie = Mysredn()
# heart = Myheartbeat(100, 50, 0.95, 5)
z = exem.get_l2NEW()  # получает словарь котиров

day0 = -1


count=0
while True:
	count+=1
	try:
		data = next(z)  # это якобы на серваке - к нему нужен доступ
		tme = exem.ttime  # Эмуляция получения времени
		day = exem.day
		#  эмуляция получения списка инструментов  раз в день
		if day != day0:
			day0 = day
			year=exem.year
			month=exem.mon
			rez =get_fut(tme)


			for mysym in mysyms:
				instdict[mysym] = dict()
				for key2 in myklaster:
					for inst in rez[mysym][key2]:
						instdict[mysym][inst]=dict()
						instdict[mysym][inst]['dat']=None
			print(instdict)

		for mysym in instdict:
			for inst in instdict[mysym]:
				if inst in data :
					instdict[mysym][inst]['dat'] = data[inst]
				else:
					instdict[mysym][inst]['dat'] = None
		# отправка словаря для добавления таймштампов tmstp [50% - те медианная задержка , 95%, текущая задержка]
		# a = heart.get_heartbeats(dt, tme)
		print(instdict)
		if count > 100:
			quit()
	except:
		print('error')
		quit()
		