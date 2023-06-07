from One_inst_class2  import Myinst
from GENERAL.G_FUNC import *
import datetime
import time

def gettm(z):
	'''получает путь , возвращает время в юникод'''
	x = z.split('\\')
	l = len(x)
	year = int(x[l - 4])
	mon = int(x[l - 3])
	day = int(x[l - 2])
	hr = int(x[l - 1].split('.')[0])
	tm = int(time.mktime(datetime.datetime(year, mon, day, hr).timetuple()))
	return tm


markets=['FRTS']
minutki=0
onlymerge=0
instrument = 'Si-6.23*FRTS'
# 'SBRF-6.23'
start_year, start_month, start_day, start_hour = 2023, 5, 23, 12
stop_year, stop_month, stop_day, stop_hour = 	 2023, 5, 23, 20
fixkf=1
getpath = 'G:\\DATA_SBOR' if system() == 'Windows' else '/media/roman/J/DATA_SBOR'



stper=60 if minutki else 3600
content = getdata_merge(onlymerge,minutki,markets,getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)

print(content)


ch_inst=Myinst(instrument,300)



for cont in content:
	tm = gettm(cont[0])
	a=get_dict(cont)

	if instrument in a:
		print('YES')
	else:
		print("NO instrument in data")
		quit()

	for key in a[instrument]:
		utime=tm+int(key)
		ch_inst.takedata(utime,a[instrument][key])


ch_inst.chartdt()











