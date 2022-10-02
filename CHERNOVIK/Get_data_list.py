from FUNC import *
getpath = '/media/roman/J/OLDHIST/FONDA'

start_year = 2020
start_month = 4
start_day = 2
start_hour = 12

stop_year = 2020
stop_month = 4
stop_day = 10
stop_hour = 1

listfiles= getdata(getpath,start_year,start_month,start_day,start_hour,stop_year,stop_month,stop_day,stop_hour)


print(listfiles)