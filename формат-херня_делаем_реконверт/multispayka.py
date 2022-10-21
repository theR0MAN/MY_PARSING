'''
ПОЛУЧАЕМ АСКИ И БИДЫ в спайке
'''
from MAIN.FUNC import *

import plotly.express as px
import lzma as lz
import json

period = 1
ONE_INST = True #(ask+bid)/2
CHANK_HOURS=1

instruments = [ 'Si-']
NOT_instruments = ['@']
getpath = '/media/roman/J/NewrOLDHIST/FORTSALL'

start_year, start_month, start_day, start_hour = 2021, 11, 16, 16
stop_year, stop_month, stop_day, stop_hour =     2021, 11, 17, 20

content = getdata(getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)

# ch=0
# Z=dict()
# data=dict()


asks={}
bids={}
last_ask={}
last_bid={}
sumlen=0
first =False
for name in content:
    # print(name)
    with lz.open(name) as f:
        a = dict(json.loads(lz.decompress(f.read()).decode('utf-8')))
    print('len(a)=  ',  len(a))
    fist_key = next(iter(a))
    ln = len(a[fist_key])
    sumlen+=ln
# фигачим аски и биды
    if not first:
        for key in a:
            for dcts in a[key]:
                if key not in asks:
                    asks[key] =[]
                    bids[key] = []
                if dcts != ['r']:
                    last_ask[key]=dcts['a']
                    last_bid[key]=dcts['b']
                    asks[key].append(last_ask[key])
                    bids[key].append(last_bid[key])
                else:
                    asks[key].append(last_ask[key])
                    bids[key].append(last_bid[key])
        first=True
    else:
        for key in asks:
            if key in a:
                for dcts in a[key]:
                    if dcts != ['r']:
                        last_ask[key]=dcts['a']
                        last_bid[key]=dcts['b']
                        asks[key].append(last_ask[key])
                        bids[key].append(last_bid[key])
                    else:
                        asks[key].append(last_ask[key])
                        bids[key].append(last_bid[key])
            else:
                # print(key,' умножаем ',last_ask[key], '   ',last_bid[key])
                asks[key]+= [last_ask[key]] * ln
                bids[key]+= [last_bid[key]] * ln

# n=-1
# for key in asks:
#     n+=1
#     if n==22:
#
#         print(len(asks[key]))
#         print(len(bids[key]))
#         print(key)
#         print(sumlen)
#         break
