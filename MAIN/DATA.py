from MAIN.FUNC import *

import plotly.express as px
import lzma as lz
import json

HOURS = True
instruments = [ 'SBPR-3.22',  'SBRF-3.22']
NOT_instruments = ['@']
period = 0
getpath = '/media/roman/J/rOLDHIST/FORTSALL'

start_year, start_month, start_day, start_hour = 2021, 11, 17, 20
stop_year, stop_month, stop_day, stop_hour =     2021, 11, 17, 20

content = getdata(getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
instrums = set()
if HOURS:
    for name in content:
        print(name)
        with lz.open(name) as f:
            a = dict(json.loads(lz.decompress(f.read()).decode('utf-8')))

        k = 0
        T0 = 0

        data = dict()
        actual_prices = dict()
        for key in a:
            T = int(key)
            for instr in a[key]:
                instrums.add(instr['i'])
                for ix in instruments:
                    for nix in NOT_instruments:
                        if ix in instr['i'] and nix not in instr['i']:
                            if 'a' in instr and 'b' in instr:
                                actual_prices[instr['i']] = (instr['a'], instr['b'])
                            else:
                                actual_prices[instr['i']] = (instr['l'], instr['l'])

            if T > T0 + period:
                T0 = T
                k += 1
                for ky in actual_prices:
                    if ky in data:
                        data[ky][0].append(k)
                        data[ky][1].append(actual_prices[ky][0] * data[ky][3])
                        data[ky][2].append(actual_prices[ky][1] * data[ky][3])
                    else:
                        if actual_prices[ky][0] > 0 and actual_prices[ky][1] > 0:
                            kf = 100 / ((actual_prices[ky][0] + actual_prices[ky][1]) / 2)
                            data[ky] = [], [], [], kf
                            data[ky][0].append(k)
                            data[ky][1].append(actual_prices[ky][0] * kf)
                            data[ky][2].append(actual_prices[ky][1] * kf)

        print('start')
        color = get_color()
        fig = px.line()
        # width=3840*4,height=2160*2
        for ky in data:
            clr = color()
            fig.add_scatter(x=data[ky][0], y=data[ky][1], line_color=clr, name=ky + ' ask')
            fig.add_scatter(x=data[ky][0], y=data[ky][2], line_color=clr, name=ky + ' bid')

        fig.show()
else:
    a = dict()
    for name in content:
        with lz.open(name) as f:
            b = dict(json.loads(lz.decompress(f.read()).decode('utf-8')))
            a.update(b)

    k = 0
    T0 = 0

    data = dict()
    actual_prices = dict()
    for key in a:
        T = int(key)
        for instr in a[key]:
            instrums.add(instr['i'])
            for ix in instruments:
                for nix in NOT_instruments:
                    if ix in instr['i'] and nix not in instr['i']:
                        if 'a' in instr and 'b' in instr:
                            actual_prices[instr['i']] = (instr['a'], instr['b'])
                        else:
                            actual_prices[instr['i']] = (instr['l'], instr['l'])

        if T > T0 + period:
            T0 = T
            k += 1
            for ky in actual_prices:
                if ky in data:
                    data[ky][0].append(k)
                    data[ky][1].append(actual_prices[ky][0] * data[ky][3])
                    data[ky][2].append(actual_prices[ky][1] * data[ky][3])
                else:
                    if actual_prices[ky][0] > 0 and actual_prices[ky][1] > 0:
                        kf = 100 / ((actual_prices[ky][0] + actual_prices[ky][1]) / 2)
                        data[ky] = [], [], [], kf
                        data[ky][0].append(k)
                        data[ky][1].append(actual_prices[ky][0] * kf)
                        data[ky][2].append(actual_prices[ky][1] * kf)

    print('start')
    color = get_color()
    fig = px.line()
    # width=3840*4,height=2160*2
    for ky in data:
        clr = color()
        fig.add_scatter(x=data[ky][0], y=data[ky][1], line_color=clr, name=ky + ' ask')
        fig.add_scatter(x=data[ky][0], y=data[ky][2], line_color=clr, name=ky + ' bid')

    fig.show()

a = list(instrums)
a.sort()
print(a)
