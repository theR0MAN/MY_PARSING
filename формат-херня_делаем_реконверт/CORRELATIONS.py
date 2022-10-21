'''
ПОЛУЧАЕМ АСКИ И БИДЫ в спайке
'''
from MAIN.FUNC import *

import plotly.express as px
import lzma as lz
import json
import pandas as pd
import numpy as np
import time

period = 1
ONE_INST = True #(ask+bid)/2
CHANK_HOURS=1

instruments = [ 'Si-']
NOT_instruments = ['@']

# getpath = '/media/roman/J/NewrOLDHIST/FORTSALL'
# start_year, start_month, start_day, start_hour = 2021, 11, 17, 10
# stop_year, stop_month, stop_day, stop_hour =     2021, 11, 17, 20

getpath = '/media/roman/J/NewrOLDHIST/FONDA'
start_year, start_month, start_day, start_hour = 2019, 4, 2, 1
stop_year, stop_month, stop_day, stop_hour =     2019, 4, 2, 20



content = getdata(getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)

# ch=0
# Z=dict()
# data=dict()

midl={}
asks={}
bids={}
last_ask={}
last_bid={}
last_midl={}
sumlen=0
first =False
for name in content:
    print(name)
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
                    midl[key] = []
                if dcts != ['r']:
                    last_ask[key]=dcts['a']
                    last_bid[key]=dcts['b']
                    last_midl[key]=(dcts['a']+dcts['b'])/2
                    asks[key].append(last_ask[key])
                    bids[key].append(last_bid[key])
                    midl[key].append(last_midl[key])
                else:
                    asks[key].append(last_ask[key])
                    bids[key].append(last_bid[key])
                    midl[key].append(last_midl[key])
        first=True
    else:
        for key in asks:
            if key in a:
                for dcts in a[key]:
                    if dcts != ['r']:
                        last_ask[key] = dcts['a']
                        last_bid[key] = dcts['b']
                        last_midl[key] = (dcts['a'] + dcts['b']) / 2
                        asks[key].append(last_ask[key])
                        bids[key].append(last_bid[key])
                        midl[key].append(last_midl[key])
                    else:
                        asks[key].append(last_ask[key])
                        bids[key].append(last_bid[key])
                        midl[key].append(last_midl[key])
            else:
                # print(key,' умножаем ',last_ask[key], '   ',last_bid[key])
                asks[key]+= [last_ask[key]] * ln
                bids[key]+= [last_bid[key]] * ln
                midl[key] += [last_midl[key]] * ln


for key in midl:
    print(' len ',key, "  ",len(midl[key]) )

timer= time.time()
df = pd.DataFrame(midl)
M = df.corr()
print('time ',time.time()-timer)

pd.set_option("display.max_rows", 10000)
pd.set_option("display.max_columns", 10000)
pd.options.display.expand_frame_repr = False


with open('corrr.txt',mode='w') as f:
    for i in M.columns:
        z = dict(M[i].sort_values(ascending=False))
        m={}
        for key in z:
            if abs(z[key])>0.7:
                m[key]=z[key]
        if len(m)>2:
            f.write(str(m)+ '\n')

# abs(x)