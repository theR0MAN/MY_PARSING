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
# markets=['MOEX2', 'FRTS2', 'CURcross', 'USAFUT', 'CUR', 'RAW', 'FxMETBR', 'FxCUR']
myklaster=['MAIN','NEAR','USAFUT','FAR']
mysyms = ['GD', 'SV', 'BR', 'NG', 'W4', 'Eu', 'Si', 'MX','ED','SR' ]

markets=['MOEX2', 'FRTS2', 'CURcross', 'USAFUT', 'CUR', 'RAW', 'FxMETBR', 'FxCUR']
# markets = ['FRTS2']  # ,'MOEX'
instdict=dict()

minutki = 0
onlymerge = 0


start_year, start_month, start_day, start_hour = 2024, 2, 1, 4
stop_year, stop_month, stop_day, stop_hour = 	 2024, 2, 14, 20

content = getdata_merge(onlymerge, minutki, markets, 'G:\\DATA_SBOR', start_year, start_month, start_day, start_hour, stop_year,
						stop_month, stop_day, stop_hour)
print(content)



exem = Getl2(content,200,0.95,10)
# scie = Mysredn()
z = exem.get_l2NEW()  # получает словарь котиров
day0 = -1
count=0
ct=0

razrez=0
countrr=0

obryv=dict()
paintdict={}
# подготовка словаря отрисовки
ixes=[]
for mysym in mysyms:
	paintdict[mysym] = dict()

fixperiod=550000
countper=0
while True:

	count+=1
	try:
		# timer=time.time()
		data = next(z)  # это якобы на серваке - к нему нужен доступ
		# print(time.time()-timer)
		tme = exem.ttime  # Эмуляция получения времени
		day = exem.day
		#  эмуляция получения списка инструментов  раз в день
		if day != day0:
			day0 = day
			year=exem.year
			month=exem.mon
			rez =get_fut(tme)

			# подготовка словаря
			for mysym in mysyms:
				instdict[mysym] = dict()
				for myklast in myklaster:
					for inst in rez[mysym][myklast]:
						instdict[mysym][inst]=None

						if inst not in obryv:
							obryv[inst] = dict()
							obryv[inst]['writeflag']=False
							obryv[inst]['timelist'] = []

						if inst not in paintdict[mysym]:
							paintdict[mysym][inst]=dict()
							paintdict[mysym][inst]['asks']=list()
							paintdict[mysym][inst]['bids'] = list()
							paintdict[mysym][inst]['fixkoef'] =None
							paintdict[mysym][inst]['fixfact'] = False

		#  приводим в одну точку  через период fixperiod
		countper += 1
		if countper>fixperiod:
			countper=0
			for mysym in paintdict:
				for inst in paintdict[mysym]:
					paintdict[mysym][inst]['fixfact'] = False
									

		countrr+=1
		if countrr>razrez:
			countrr=0
			ct+=1
			ixes.append(ct)
			for mysym in instdict:
				for inst in instdict[mysym]:
					if inst in data :
						instdict[mysym][inst] = data[inst]
						# мониторинг обрывов
						if instdict[mysym][inst]['tmstp'][0] != None:
							if instdict[mysym][inst]['tmstp'][2] :
								obryv[inst]['writeflag'] = False
							if  instdict[mysym][inst]['tmstp'][2]==False and obryv[inst]['writeflag']==False:
								# print(inst, instdict[mysym][inst]['tmstp'], "  ",datetime.datetime.fromtimestamp(tme).strftime('%Y-%m-%d %H:%M:%S'))
								obryv[inst]['writeflag'] = True
								obryv[inst]['timelist'].append([tme,datetime.datetime.fromtimestamp(tme).strftime('%Y-%m-%d %H:%M:%S')])




						# if instdict[mysym][inst]['tmstp'][0]!=None:
						# 	if instdict[mysym][inst]['tmstp'][0] * 5 > instdict[mysym][inst]['tmstp'][1]:
						# 		obryv[inst]['writeflag'] = False
						# 	if instdict[mysym][inst]['tmstp'][0]*5 < instdict[mysym][inst]['tmstp'][1] and obryv[inst]['writeflag']==False:
						# 		# print(inst, instdict[mysym][inst]['tmstp'], "  ",datetime.datetime.fromtimestamp(tme).strftime('%Y-%m-%d %H:%M:%S'))
						# 		obryv[inst]['writeflag'] = True
						# 		obryv[inst]['timelist'].append([tme,datetime.datetime.fromtimestamp(tme).strftime('%Y-%m-%d %H:%M:%S')])


						# print(inst,data[inst]['dat'],'  +  ',paintdict[mysym][inst]['fixfact'])
						if data[inst]['dat']!=None and paintdict[mysym][inst]['fixfact'] == False:
							paintdict[mysym][inst]['fixkoef'] = 200/(data[inst]['dat'][0]+data[inst]['dat'][1])
							paintdict[mysym][inst]['fixfact'] = True

						if paintdict[mysym][inst]['fixfact'] :
							if obryv[inst]['writeflag'] == False:
								paintdict[mysym][inst]['asks'].append(data[inst]['dat'][0]*paintdict[mysym][inst]['fixkoef'])
								paintdict[mysym][inst]['bids'].append(data[inst]['dat'][1]*paintdict[mysym][inst]['fixkoef'])
							else:
								paintdict[mysym][inst]['asks'].append(None)
								paintdict[mysym][inst]['bids'].append(None)
						else:
							paintdict[mysym][inst]['asks'].append(None)
							paintdict[mysym][inst]['bids'].append(None)
					else:
						paintdict[mysym][inst]['asks'].append(None)
						paintdict[mysym][inst]['bids'].append(None)


	# except:
	except Exception:
		print(traceback.format_exc())
		print('error')
		break
		# quit()
print('stop')

for inst in obryv:
	print('obryv ',inst,len(obryv[inst]['timelist']),obryv[inst]['timelist'])

#
for mysym in paintdict:
	color = get_color()
	fig = px.line()
	for inst in paintdict[mysym] :
		clr = color()
		fig.add_scatter(x=ixes, y=paintdict[mysym][inst]['asks'], line_color=clr, name=inst+' ask')
		fig.add_scatter(x=ixes, y=paintdict[mysym][inst]['bids'], line_color=clr, name=inst+' bid')
	fig.show()