# зачача -распараллелить распаковку, синх мап  , распаковывать порциями - чтобы оперативы  хватило, но
# не больше чем ядер за раз
# а потом скармливать по одному в общее тело - для  тестера понадобится
from multiprocessing import Pool
from PROJECT.TEST.Test_lib import getdata_merge
from Viz_lib import get_color
from platform import system
import plotly.express as px
import lzma
import json
import time



markets=['FRTS']  #,'MOEX'
minutki=0
onlymerge=0
in_instruments = ['NG-']
	# [ 'NG-1.23*FRTS',  'NG-2.23*FRTS',  'NG-3.23*FRTS']
not_in_instruments = ['HANG']
start_year, start_month, start_day, start_hour = 2023, 9, 22, 8
stop_year, stop_month, stop_day, stop_hour = 	 2023, 9, 22, 14
fixkf=1



getpath = 'G:\\DATA_SBOR' if system() == 'Windows' else '/media/roman/J/DATA_SBOR'
content = getdata_merge(onlymerge,minutki,markets,getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
timer2=time.time()

def Func(cont):
	lz=lzma
	a=dict()
	for name in cont:
		with lz.open(name) as f:
			bb = dict(json.loads(lz.decompress(f.read()).decode('utf-8')))
		a |= bb
	return dict([(cont[0],len(a))])



if __name__ == '__main__':
	print(content)
	with Pool(processes=4) as pool:
		results = pool.map(Func,content)
	print(results)
	print(f" 2 time= {time.time() - timer2}")

	#
	# stper = 60 if minutki else 3600
	# data = dict()
	# nomfile = -1
	# nomfile+=1
	# for inst in a:
	# 	for ix in in_instruments:
	# 		for nix in not_in_instruments:
	# 			if ix in inst and nix not in inst:
	# 				if inst not in data:
	# 					data[inst]=dict()
	# 					data[inst]['askmas'] = []
	# 					data[inst]['bidmas'] = []
	# 					data[inst]['ixmas'] =[]
	# 				for tmp in range(stper):
	# 					data[inst]['ixmas'].append(tmp+stper*nomfile)
	# 					if str(tmp) in a[inst]:
	# 						if "kf" not in data[inst]:
	# 							try:
	# 								kf = 200 / (a[inst][str(tmp)]['asks'][0][0] + a[inst][str(tmp)]['bids'][0][0])
	# 							except:
	# 								kf = 200 / (a[inst][str(tmp)]['a'] + a[inst][str(tmp)]['b'])
	# 							kf = 1 if fixkf == False else kf
	# 							data[inst]['kf']=kf
	# 							if not minutki:
	# 								data[inst]['lastask'] = a[inst][str(tmp)]['asks'][0][0]
	# 								data[inst]['lastbid'] = a[inst][str(tmp)]['bids'][0][0]
	# 							else:
	# 								data[inst]['lastask'] = a[inst][str(tmp)]['a']
	# 								data[inst]['lastbid'] = a[inst][str(tmp)]['b']
	#
	# 						if not minutki:
	# 							data[inst]['askmas'].append(a[inst][str(tmp)]['asks'][0][0] * data[inst]['kf'])
	# 							data[inst]['bidmas'].append(a[inst][str(tmp)]['bids'][0][0] * data[inst]['kf'])
	# 							data[inst]['lastask'] = a[inst][str(tmp)]['asks'][0][0]
	# 							data[inst]['lastbid'] = a[inst][str(tmp)]['bids'][0][0]
	# 						else:
	# 							data[inst]['askmas'].append(a[inst][str(tmp)]['a'] * data[inst]['kf'])
	# 							data[inst]['bidmas'].append(a[inst][str(tmp)]['b'] * data[inst]['kf'])
	# 							data[inst]['lastask'] = a[inst][str(tmp)]['a']
	# 							data[inst]['lastbid'] = a[inst][str(tmp)]['b']
	#
	# 					else:
	# 						if "kf" in data[inst]:
	# 							data[inst]['askmas'].append(data[inst]['lastask'] * data[inst]['kf'])
	# 							data[inst]['bidmas'].append(data[inst]['lastbid'] * data[inst]['kf'])
	# 						else:
	# 							data[inst]['askmas'].append(None)
	# 							data[inst]['bidmas'].append(None)
	#
	#
	#
	#
	# 	print(list(data))
	# 	color = get_color()
	# 	fig = px.line()
	# 	for inst in data:
	# 		clr = color()
	# 		fig.add_scatter(x=data[inst]['ixmas'], y=data[inst]['askmas'], line_color=clr, name=inst + ' ask')
	# 		fig.add_scatter(x=data[inst]['ixmas'], y=data[inst]['bidmas'], line_color=clr, name=inst + ' bid')
	# 	fig.show()