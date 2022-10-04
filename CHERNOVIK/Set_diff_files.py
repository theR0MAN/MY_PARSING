from FUNC import *
import json
import multiprocessing
import time
import os
import datetime


getpath = '/media/roman/J/OLDHIST/FORTS'
putpath = '/media/roman/J/jsOLDHIST/FORTS'

start_year = 2021
start_month = 7
start_day = 1
start_hour = 10

stop_year = 2022
stop_month = 7
stop_day = 1
stop_hour = 17


content1 =getdata(getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
# print(content1)
set1=set(content1)

content2 = getdata(putpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
# print(content2)
set2=set(content2)

content21=[]
for i in content2:
    x=i.replace('jsOLDHIST','OLDHIST')
    content21.append(x)
# print(content21)
set21=set(content21)


content = list(set1.difference(set21))
print(content)
#
# print(len(diff_set))

# diff_set2 = list(set1.difference(set2))
# print(diff_set2)

# months.add("Feb")

# song = 'cold, cold heart'
# replaced_song = song.replace('o', 'e')
