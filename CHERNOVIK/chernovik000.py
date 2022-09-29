import multiprocessing
import time
import os
import datetime
from itertools import product

getpath='/media/roman/J/OLDHIST/FONDA'

start_year = 2020
start_month = 4
start_day = 1
start_hour = 12

stop_year = 2020
stop_month = 4
stop_day = 1
stop_hour = 12


listfiles=[]
flag = False
for y in range(start_year, stop_year+1):
    if flag :
        print('br y')
        break
    for m in range(start_month, 13):
        if flag :
            print('br m')
            break
        for d in range(start_day, 32):
            if flag :
                print('br d')
                break
            for h in range(start_hour, 24):
                if os.path.exists(getpath + '/' + str(y) + '/' + str(m) + '/' + str(d)+'/'+str(h)+'.txt'):
                    print(f'year  {y}  month  {m}   day  {d}  hour  {h}  ')
                    listfiles.append(getpath+'/'+str(y)+'/'+str(m)+'/'+str(d)+'/'+str(h)+'.txt')
                if y == stop_year and m == stop_month and d == stop_day and h == stop_hour:
                    flag = True
                    # print(y,'  ',m,'  ',d,'  ',h,'  ',os.path.exists(getpath + '/' + str(y) + '/' + str(m) + '/' + str(d)+'/'+str(h)+'.txt'))
                    print('br h')
                    break
            start_hour = 0
        start_day = 1
    start_month = 1

print(listfiles)
