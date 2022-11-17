from MAIN.FUNC import *

import plotly.express as px
import lzma as lz
import json

period = 1
ONE_INST = False #(ask+bid)/2
CHANK_HOURS=7

instruments = [ 'Si-']
NOT_instruments = ['@']
getpath = '/media/roman/J/NewrOLDHIST/FORTSALL'

start_year, start_month, start_day, start_hour = 2021, 11, 17, 16
stop_year, stop_month, stop_day, stop_hour =     2021, 11, 17, 20

content = getdata(getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
instrums = set()
lencont=len(content)
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
   ch+=1
   if ch<=CHANK_HOURS:
        lastname1=name
        with lz.open(name) as f:
            a = dict(json.loads(lz.decompress(f.read()).decode('utf-8')))
        print('len(a)=  ',  len(a))
        fist_key = next(iter(a))
        ln = len(a[fist_key])
        sumlen+=ln
    # фигачим аски и биды
        if not first:
            for key in a:
                instrums.add(key)
                for nix in NOT_instruments:
                    for ix in instruments:
                        for nix in NOT_instruments:
                            if ix in key and nix not in key:
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
            sp = list(instrums)
            sp.sort()
            print(sp)
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
   else:
       lastname2 = name
       # резка на периоды
       data = dict()
       for key in asks:
           kf = 200 / (asks[key][1] + bids[key][1])
           data[key] = [], [], []
           k = -1
           for i in range(0, len(asks[key]), period):
               k += 1
               data[key][0].append(k)
               data[key][1].append(asks[key][i] * kf)
               data[key][2].append(bids[key][i] * kf)

       print('start')
       color = get_color()
       fig = px.line()
       # width=3840*4,height=2160*2
       for ky in data:
           clr = color()
           if ONE_INST:
               one = []
               for i in range(len(data[ky][1])):
                   one.append((data[ky][1][i] + data[ky][2][i]) / 2)
               fig.add_scatter(x=data[ky][0], y=one, line_color=clr, name=ky)
           else:
               fig.add_scatter(x=data[ky][0], y=data[ky][1], line_color=clr, name=ky + ' ask')
               fig.add_scatter(x=data[ky][0], y=data[ky][2], line_color=clr, name=ky + ' bid')
       fig.show()

       ch = 0
       asks = {}
       bids = {}
       last_ask = {}
       last_bid = {}
       sumlen = 0
       first = False


if lastname1!=lastname2:

    data = dict()
    for key in asks:
       kf = 200 / (asks[key][1] + bids[key][1])
       data[key] = [], [], []
       k = -1
       for i in range(0, len(asks[key]), period):
           k += 1
           data[key][0].append(k)
           data[key][1].append(asks[key][i] * kf)
           data[key][2].append(bids[key][i] * kf)

    # print('start')
    color = get_color()
    fig = px.line()
    # width=3840*4,height=2160*2
    for ky in data:
       clr = color()
       if ONE_INST:
           one = []
           for i in range(len(data[ky][1])):
               one.append((data[ky][1][i] + data[ky][2][i]) / 2)
           fig.add_scatter(x=data[ky][0], y=one, line_color=clr, name=ky)
       else:
           fig.add_scatter(x=data[ky][0], y=data[ky][1], line_color=clr, name=ky + ' ask')
           fig.add_scatter(x=data[ky][0], y=data[ky][2], line_color=clr, name=ky + ' bid')
    fig.show()

    ch = 0
    asks = {}
    bids = {}
    last_ask = {}
    last_bid = {}
    sumlen = 0
    first = False