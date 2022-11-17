import math
from random import randint
from MAIN.FUNC import *
import plotly.express as px
import collections

# period=680
ixes = 50000
period =3000
shag_sr=90


koef = ixes / 5


sm = 5
ksin = 1
spread=1
twoksin=1
kugol=600

cor_period=int(period/shag_sr)
ksin2 = ksin*twoksin


x = []
yask = []
ybid = []
coresred = []
otklask= []
otklbid= []

work=False
fixcount=0
realcount=0
count = 0
sum2 = 0
sumr = 0
sumotkl = 0
index = -1

for ugol in range(0, ixes, 1):

    sn = ksin * math.sin(math.radians(ugol))
    sinusoida=sn + sm + ugol / koef+ ksin2 * math.sin(math.radians(ugol/kugol))

    ask=sinusoida
    bid=sinusoida-spread
    midl = (ask + bid) / 2

    realcount += 1
    if(fixcount<realcount):
        fixcount=realcount+shag_sr
        # fixcount=realcount+randint(1, shag_sr * 2)
        count+=1
        if count <= cor_period:
            sum2 += midl
            iesred = sum2 / count
            sumr += midl - iesred
            sredrazn = sumr / count
            vcoresred=iesred + sredrazn
            # otkl = (abs(vcoresred - ask) + abs(vcoresred - bid) - spread / 2)
            otkl = (abs(vcoresred - ask) + abs(vcoresred - bid) - spread )
            sumotkl+=otkl
            iotkl = sumotkl / count


        else:
            sum2 = sum2 - sum2 / cor_period + midl
            iesred = sum2 / cor_period
            sumr = sumr - sumr / cor_period + midl - iesred
            sredrazn = sumr / cor_period
            vcoresred = iesred + sredrazn
            # otkl = (abs(vcoresred - ask) + abs(vcoresred - bid)-spread/2)
            otkl = (abs(vcoresred - ask) + abs(vcoresred - bid) - spread )
            sumotkl= sumotkl - sumotkl / cor_period + otkl
            iotkl = sumotkl / cor_period


    x.append(ugol)
    yask.append(ask)
    ybid.append(bid)
    coresred.append(vcoresred)
    otklask.append(vcoresred + iotkl)
    otklbid.append(vcoresred - iotkl)



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



fig.show()
