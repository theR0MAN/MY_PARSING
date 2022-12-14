from FUNC import *
import json

getpath = '/media/roman/J/OLDHIST/FONDA'
path2 = '/media/roman/J/jsOLDHIST/FONDA'

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

bigdict={}
biglist=[]
timekey=''
# for i in listfiles:
#     with open(i, mode='r', encoding='utf-8') as r:
#         zl = r.readlines()


with open(listfiles[0], mode='r', encoding='utf-8') as r:
    zl = r.readlines()


for i in zl:  # пробегаеся по списку строк
    a = i.split()  # дробим каждую строку в элементы списка
    # print(a)
    if len(a) > 1:

        if(a[0]=='*'):
            # print(a)
            if timekey > '':
                # bigdict.update(timekey=biglist)
                bigdict[timekey]=biglist
                # print(biglist)
            timekey=a[1]
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
                dat = dict(i=a[1], p=a[0], l=float(a[4]), a=float(ask), b=float(bid), vl=float(a[5]), bvl=float(a[6]),
                           avl=float(a[7]), kbo=int(float(a[8])), kao=int(float(a[9])), asks=asks, bids=bids)
                biglist.append(dat)


filename=listfiles[0]
z=filename.split('/')
yr=z[6]
mon=z[7]
dy=z[8]
name=z[9]
nextpath=path2+'/'+ yr
if not os.path.exists(nextpath):
    os.mkdir(nextpath)
nextpath=nextpath+'/' + mon
if not os.path.exists(nextpath):
    os.mkdir(nextpath)
nextpath=nextpath+ '/' + dy
if not os.path.exists(nextpath):
    os.mkdir(nextpath)
fullname = nextpath+'/' +name

with open(fullname,'w') as fl:
        json.dump(bigdict, fl)

# with open(fullname, mode='r', encoding='utf-8') as r:
#     data = dict(json.load(r))
# print(data["1585823731"])
#
