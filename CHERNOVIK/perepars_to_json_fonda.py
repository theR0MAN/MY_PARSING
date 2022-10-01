from FUNC import *
import json
import multiprocessing
import time
import os
import datetime


def end_func(response):
    print("end_func:", response)


getpath = '/media/roman/J/OLDHIST/FONDA'
path2 = '/media/roman/J/jsOLDHIST/FONDA'

start_year = 2019
start_month = 1
start_day = 1
start_hour = 10

stop_year = 2021
stop_month = 1
stop_day = 22
stop_hour = 17

content = getdata(getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
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
                ind = 11
                for i in range(int(a[10])):
                    asks.append((float(a[ind]), float(a[ind + 1])))
                    ind += 2
                for i in range(int(a[ind])):
                    bids.append((float(a[ind + 1]), float(a[ind + 2])))
                    ind += 2
                if len(asks) > 0 and len(bids) > 0:
                    ask = asks[0][0]
                    bid = bids[0][0]
                    dat = dict(i=a[1], p=a[0], l=float(a[4]), a=float(ask), b=float(bid), vl=float(a[5]),
                               bvl=float(a[6]),
                               avl=float(a[7]), kbo=int(float(a[8])), kao=int(float(a[9])), asks=asks, bids=bids)
                    biglist.append(dat)


    z = filename.split('/')
    yr = z[6]
    mon = z[7]
    dy = z[8]
    name = z[9]
    nextpath = path2 + '/' + yr
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


timer = time.time()
if __name__ == '__main__':
    with multiprocessing.Pool(8) as pool:
        pool.map_async(perepars, content, callback=end_func)
        pool.close()
        pool.join()
print('ALL TIME ', time.time() - timer)
