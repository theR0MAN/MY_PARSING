from FUNC import *
import json

getpath = '/media/roman/J/OLDHIST/FONDA'

start_year = 2020
start_month = 4
start_day = 2
start_hour = 10

stop_year = 2020
stop_month = 4
stop_day = 2
stop_hour = 10

listfiles = getdata(getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
print(listfiles)

biglist=[]

for i in listfiles:
    with open(i, mode='r', encoding='utf-8') as r:
        zl = r.readlines()

for i in zl:  # пробегаеся по списку строк
    a = i.split()  # дробим каждую строку в элементы списка
    # print(a)

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
            dat = dict(i=a[1], p=a[0], l=float(a[4]), a=float(ask), b=float(bid), vl=float(a[5]), bvl=float(a[6]),
                       avl=float(a[7]), kbo=int(float(a[8])), kao=int(float(a[9])), asks=asks, bids=bids)
            # biglist.append(dat)
            # json_string = json.dumps(dat)
            # print(json_string)

            # data = dict(json.loads(json_string))
            # print(data)
# print(biglist)