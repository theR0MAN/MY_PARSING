import math
from MAIN.FUNC import *
import plotly.express as px
import collections

# period=680
ixes = 50000
eperiod =5000
koef = ixes / 50


sm = 5
ksin = 1
spread=0.5
twoksin=1
kugol=600

ksin2 = ksin*twoksin


x = []
yask = []
ybid = []
midl=[]
esred = []
coresred = []
sredcoresred = []

otklask= []
otklbid= []



for ugol in range(0, ixes, 1):
    sn = ksin * math.sin(math.radians(ugol))
    x.append(ugol)
    sinusoida=sn + sm + ugol / koef+ ksin2 * math.sin(math.radians(ugol/kugol))
    yask.append(sinusoida)
    ybid.append(sinusoida-spread)
    midl.append(sinusoida-spread/2)



count = 1
sum2 = 0
sumr = 0
sumotkl=0
index=-1
sumcoresred=0

for iy in midl:
    index+=1
    if count <= eperiod:
        sum2 += midl[index]
        iesred = sum2 / count
        # esred.append(iesred)

        sumr += midl[index] - iesred
        sredrazn = sumr / count

        vcoresred=iesred + sredrazn
        coresred.append(vcoresred)

        sumcoresred+=vcoresred
        isumsred = sumcoresred / count
        sredcoresred.append(isumsred)

        # otkl=(abs(vcoresred-yask[index])+abs(vcoresred-ybid[index]))/2
        otkl = (abs(vcoresred - yask[index]) + abs(vcoresred - ybid[index]) - spread / 2)
        sumotkl+=otkl
        iotkl = sumotkl / count
        otklask.append(vcoresred+iotkl)
        otklbid.append(vcoresred-iotkl)

    else:
        sum2 = sum2 - sum2 / eperiod + midl[index]
        iesred = sum2 / eperiod
        # esred.append(iesred)

        sumr = sumr - sumr / eperiod + midl[index] - iesred
        sredrazn = sumr / eperiod

        vcoresred = iesred + sredrazn
        coresred.append(vcoresred)

        sumcoresred =sumcoresred- sumcoresred/ eperiod  +vcoresred
        isumsred = sumcoresred / eperiod
        sredcoresred.append(isumsred)

        # otkl=(abs(vcoresred-yask[index])+abs(vcoresred-ybid[index]))/2
        otkl = (abs(vcoresred - yask[index]) + abs(vcoresred - ybid[index])-spread/2)
        sumotkl=sumotkl-sumotkl/eperiod+ otkl
        iotkl = sumotkl / eperiod
        otklask.append(vcoresred+iotkl)
        otklbid.append(vcoresred-iotkl)

    count += 1

# =========================================================================================


color = get_color()
fig = px.line()

clr = color()
fig.add_scatter(x=x, y=yask, line_color=clr, name='SINask')
clr = color()
fig.add_scatter(x=x, y=ybid, line_color=clr, name='SINbid')

clr = color()
fig.add_scatter(x=x, y=coresred, line_color=clr, name='coresred')

clr = color()
clr = color()
fig.add_scatter(x=x, y=otklask, line_color=clr, name='otklask')
fig.add_scatter(x=x, y=otklbid, line_color=clr, name='otklbid')

# clr = color()
# fig.add_scatter(x=x, y=sredcoresred, line_color=clr, name='sredcoresred')

fig.show()
