
from MAIN.FUNC import *

import plotly.express as px
import lzma as lz
import json


ONE_INST = False #(ask+bid)/2


instrument = 'AGRO*MOEX'
getpath = '/media/roman/J/greatOLDHIST/FONDA'

start_year, start_month, start_day, start_hour = 2020, 10, 16, 12
stop_year, stop_month, stop_day, stop_hour =     2020, 10, 16, 12

content = getdata(getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
instrums = list()

x=[]
ask=[]
bid=[]
ask2=[]
bid2=[]

ix =0
for name in content:
    with lz.open(name) as f:
        a = dict(json.loads(lz.decompress(f.read()).decode('utf-8')))
    for instr in a:
        if instr not in instrums:
            instrums.append(instr)
    instrums.sort()
    print(name,"   ",instrums)

    if instrument in instrums:
        print("YES ",instrument)

        for  timestamp in a[instrument]:
            ix+=1
            x.append(ix)
            ask.append(a[instrument][timestamp]['a'])
            bid.append(a[instrument][timestamp]['b'])
            ask2.append(a[instrument][timestamp]['asks'][1][0])
            bid2.append(a[instrument][timestamp]['bids'][1][0])
    else:
        print("NO  ", instrument)

        # print( timestamp,"  ",
        #        a[instrument][timestamp]['a'] ,"  ",a[instrument][timestamp]['asks'][1][0] ,"  ",
        #        a[instrument][timestamp]['b'],"  ",a[instrument][timestamp]['bids'][1][0] )

fig = px.line()
color = get_color()
clr = color()

fig.add_scatter(x=x, y=ask, line_color=clr, name=instrument + ' ask')
fig.add_scatter(x=x, y=bid, line_color=clr, name=instrument + ' bid')
clr = color()
fig.add_scatter(x=x, y=ask2, line_color=clr, name=instrument + ' ask2')
fig.add_scatter(x=x, y=bid2, line_color=clr, name=instrument + ' bid2')

fig.show()