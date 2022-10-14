
import plotly.express as px
import lzma
import json

name='/media/roman/J/rOLDHIST/FONDA/2020/5/12/14.roman'
lz=lzma
with lz.open(name) as f:
    a=dict(json.loads(lz.decompress(f.read()).decode('utf-8')))

k=0
T0=0
period=0

data = dict()
actual_prices=dict()
for key in a:
    T=int(key)
    for instr in a[key]:
        if (instr['i'] == 'SBER'):
            actual_prices[instr['i']]=instr['l']

    if T>T0+period:
        T0=T
        k+=1
        for ky in actual_prices:
            if ky in data:
                data[ky][0].append(k)
                data[ky][1].append(actual_prices[ky] * data[ky][2])
            else:
                if actual_prices[ky]>0:
                    kf= 100 / actual_prices[ky]
                    data[ky]=[],[],kf
                    data[ky][0].append(k)
                    data[ky][1].append(actual_prices[ky] * kf)


print('start')
fig = px.line(width=3840*2,height=2160*2)

for ky in data:
    fig.add_scatter(x=data[ky][0], y=data[ky][1],name =ky)


fig.show()
#
