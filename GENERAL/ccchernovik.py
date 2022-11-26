from G_FUNC import *

minutki=1
onlymerge=0
markets=['FRTS','MOEX','MOEX2']
getpath = 'G:\\DATA_SBOR'

start_year, start_month, start_day, start_hour = 2022, 11, 25, 7
stop_year, stop_month, stop_day, stop_hour = 	 2022, 11, 25, 20

content = getdata_merge(onlymerge,minutki,markets,getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
print(content)