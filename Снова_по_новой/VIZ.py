
from MAIN.FUNC import *

import plotly.express as px
import lzma as lz
import json


ONE_INST = False #(ask+bid)/2


instruments = [ 'NKNCP*MOEX', 'KOGK*MOEX']
NOT_instruments = ['@']
getpath = '/media/roman/J/greatOLDHIST/FONDA'

start_year, start_month, start_day, start_hour = 2020, 10, 15, 10
stop_year, stop_month, stop_day, stop_hour =     2020, 10, 15, 10

content = getdata(getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
instrums = set()
# lencont=len(content)
lastname1=str()
lastname2=str()

ch=0
asks={}
bids={}
last_ask={}
last_bid={}
sumlen=0
first =False
for name in content:
    with lz.open(name) as f:
        a = dict(json.loads(lz.decompress(f.read()).decode('utf-8')))
    # print(name,'  len(a)=  ',  len(a))
    fist_key = next(iter(a))
    fist_key2=int(next(iter(a[next(iter(a))])))
    print(fist_key)
    print(fist_key2)
    #
    # fist_key2=next(iter(a[next(iter(a))]))
    # print(fist_key2)
    cnt=10
    cnt0=0
    for ky in a[fist_key]:
        print(ky,'  ask = ',a[fist_key][ky]['a'],'  bid = ',a[fist_key][ky]['b']  )
        print(ky, '  asks = ', a[fist_key][ky]['asks'][0][0], '  bids = ', a[fist_key][ky]['bids'][0][0])
        print(ky, '  asks2 = ', a[fist_key][ky]['asks'][1][0], '  bids2 = ', a[fist_key][ky]['bids'][1][0])
        cnt0+=1
        if cnt0>cnt:
            break

    ky=11
    for ki in range (ky,-1,-1):
        ki2 = str(ki)
        if ki2 in a[fist_key]:
            print(ki, ' ZZZ ask = ', a[fist_key][ki2]['a'], '  bid = ', a[fist_key][ki2]['b'])
            break
    else:
        print('NO FLAGS')


