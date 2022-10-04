from FUNC import *
import json
import multiprocessing
import time
import os
import datetime


def end_func(response):
    print("end_func:", response)



getpath = '/media/roman/J/jsOLDHIST/FORTSALL'

start_year = 2021
start_month = 7
start_day = 1
start_hour = 10

stop_year = 2022
stop_month = 7
stop_day = 1
stop_hour = 17

content = getdata(getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)


for i in content:
    newname=i.replace('.txt','.json')
    os.rename(i,newname)
    print(newname)
