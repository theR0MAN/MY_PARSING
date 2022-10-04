from FUNC import *
import json
import multiprocessing
import time
import os
import datetime


def end_func(response):
    print("end_func:", response)


getpath = '/media/roman/J/OLDHIST/FORTS'
putpath = '/media/roman/J/jsOLDHIST/FORTS'

start_year = 2021
start_month = 5
start_day = 1
start_hour = 10

stop_year = 2022
stop_month = 7
stop_day = 1
stop_hour = 17

# content = getdata(getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
# print(content)

content1 =getdata(getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
set1=set(content1)
content2 = getdata(putpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
set2=set(content2)
content21=[]
for i in content2:
    x=i.replace('jsOLDHIST','OLDHIST')
    content21.append(x)
set21=set(content21)
content = list(set1.difference(set21))
print(content)

def perepars(i):
    filename = i
    bigdict = {}
    biglist = []
    timekey = ''
    with open(i, mode='r', encoding='utf-8') as r:
        zl = r.readlines()
    for i in zl:  # пробегаеся по списку строк
        a = i.split()  # дробим каждую строку в элементы списка
        if len(a) > 1:
            if (a[0] == '*'):
                if timekey > '':
                    bigdict[timekey] = biglist
                timekey = a[1]
                biglist = []
            if len(a) > 2:
                asks = []
                bids = []
                ind = 5
                for i in range(int(a[4])):
                    asks.append((float(a[ind]), float(a[ind + 1])))
                    ind += 2
                for i in range(int(a[ind])):
                    bids.append((float(a[ind + 1]), float(a[ind + 2])))
                    ind += 2
                if len(asks) > 0 and len(bids) > 0:
                    ask = asks[0][0]
                    bid = bids[0][0]
                    dat = dict(i=a[1],p=a[0],a=float(ask),b=float(bid),asks=asks,bids=bids)
                    biglist.append(dat)


    z = filename.split('/')
    yr = z[6]
    mon = z[7]
    dy = z[8]
    name = z[9]
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

    with open(fullname, 'w', encoding='utf-8') as fl:
        json.dump(bigdict, fl)
        print(fullname)
    return filename


timer = time.time()
if __name__ == '__main__':
    with multiprocessing.Pool(4) as pool:
        pool.map_async(perepars, content, callback=end_func)
        pool.close()
        pool.join()
print('ALL TIME ', time.time() - timer)
