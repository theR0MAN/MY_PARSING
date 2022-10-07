from FUNC import *
import json
import multiprocessing
import time
import os
import lzma
import datetime


def end_func(response):
    print("end_func:", response)


getpath = '/media/roman/J/jsOLDHIST/FORTSALL'
putpath = '/media/roman/J/rOLDHIST/FORTSALL'

start_year = 2021
start_month = 8
start_day = 1
start_hour = 1

stop_year = 2022
stop_month = 7
stop_day = 1
stop_hour = 1

# start_year = 2019
# start_month = 1
# start_day = 3
# start_hour = 10
#
# stop_year = 2019
# stop_month = 1
# stop_day = 3
# stop_hour = 18


content1 =getdata(getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
set1=set(content1)
content2 =getdata(putpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
set2=set(content2)
content21=[]
for i in content2:
    x=i.replace('rOLDHIST','jsOLDHIST').replace('.roman','.json')
    content21.append(x)
set21=set(content21)
content = list(set1.difference(set21))
print(content)

ln=len(content)
val = multiprocessing.Value('d', ln)


def perepars(i):
    timer = time.time()
    lz=lzma
    filename = i
    with open(i, mode='r') as f:
        a = lz.compress(f.read().encode('utf-8'))


    z = filename.split('/')
    yr = z[6]
    mon = z[7]
    dy = z[8]
    name = z[9].replace('.json', '.roman')

    nextpath = putpath + '/' + yr
    if not os.path.exists(nextpath):
        os.mkdir(nextpath)
    nextpath = nextpath + '/' + mon
    if not os.path.exists(nextpath):
        os.mkdir(nextpath)
    nextpath = nextpath + '/' + dy
    if not os.path.exists(nextpath):
        os.mkdir(nextpath)
    fullname = nextpath + '/' + name

    with lz.open(fullname, "w") as f:
        f.write(a)
    val.value = val.value - 1
    print(val.value,' ' ,multiprocessing.current_process().name,"  ", fullname,' time: ', time.time() - timer)
    return fullname



if __name__ == '__main__':
    with multiprocessing.Pool(8) as pool:
        pool.map_async(perepars, content, callback=end_func)
        pool.close()
        pool.join()

