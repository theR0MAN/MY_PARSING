from MAIN.FUNC import *
import json
import multiprocessing
import time
import os
import lzma
import datetime


nohour=9
previous=0
content2=[]

def xname (adres):
    lis = adres.split('/')
    lis[-1]='INSTRMENTS.txt'
    return '/'.join(lis)


getpath = '/media/roman/J/greatOLDHIST/FORTS'

start_year, start_month, start_day, start_hour = 2021, 6, 1, 1
stop_year, stop_month, stop_day, stop_hour =     2022, 7, 1, 1

content = getdata(getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
print(content)

# get only first hours in every day for get instruments besides 9
for adres in content:
    list0=adres.split('/')
    list=list0[-4:]
    # print(list)
    ff=list[3].split('.')
    # print(ff[0])
    if previous!=list[2] and int(ff[0])>nohour :#and not os.path.exists(xname(adres))
        previous=list[2]
        content2.append(adres)
print(content2)

ln = len(content2)
val = multiprocessing.Value('d', ln)

def perepars(i):
    xxname=xname
    lz = lzma
    inslist=[]
    with lz.open(i) as f:
        a = dict(json.loads(lz.decompress(f.read()).decode('utf-8')))

        for key in a:
            inslist.append((key+"  "+ str(len(a[key]))))
            inslist.sort()


    with open(xxname(i),mode='w') as f:
        for line in inslist:
            f.write(line+'\n')

    val.value = val.value - 1
    print(val.value, '  ',xxname(i))



if __name__ == '__main__':
    with multiprocessing.Pool(8) as pool:
        pool.map_async(perepars, content2)
        pool.close()
        pool.join()