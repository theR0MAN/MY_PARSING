# from  my_filter_instrs import  *
from my_kriptofun import *

# a= myload('8')
# for sym in a:
# 	print(sym,a[sym])
# 	break

from PROJECT.TEST.Test_lib import *
from PROJECT.VIZUAL.Viz_lib import get_color
from PROJECT.SCIENTIC.sc_sredn_lib import *
from platform import system
import plotly.express as px
from collections import deque
import datetime, time  # timer=time.time()
import traceback


pth='G:\\NEWKRIPT'

markets = os.listdir(pth)
# markets = ['binance', 'binanceusdm', 'bingx', 'bybit', 'huobi', 'kucoinfutures', 'whitebit']  #'poloniex',24 1  7-10
print(markets)

# markets = ['FRTS2']  # ,'MOEX'
instdict = dict()

minutki = 123
onlymerge = 0

start_year, start_month, start_day, start_hour = 2024, 3, 18, 8
stop_year, stop_month, stop_day, stop_hour = 2024, 3, 18, 8

content = getdata_merge(onlymerge, minutki, markets, pth, start_year, start_month, start_day, start_hour, stop_year,
						stop_month, stop_day, stop_hour)
print(content)

if content==[]:
	print(' нет данных за этот период' )
	quit()

exem = Getl2(content, 200, 0.95, 10)
# scie = Mysredn()
z = exem.get_l3()  # получает словарь котиров
day0 = -1
count = 0
ct = 0

razrez = 0
countrr = 0

obryv = dict()
paintdict = {}
# подготовка словаря отрисовки
ixes = []


first=False
instset=set()

limgraf=5 # минимум графиков в окне
while True:

	count += 1
	try:
		data = next(z)  # это якобы на серваке - к нему нужен доступ
		for sym in data:
			if data[sym]['dat']!=None:
				print(sym, data[sym])
		# print(data)
		# if count>100:
		# break
	except Exception:
		print(traceback.format_exc())
		print('error')
		break