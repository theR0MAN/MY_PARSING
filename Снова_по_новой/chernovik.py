import math
from MAIN.FUNC import *
import plotly.express as px
import collections

# period=680
ixes=60000
koef=ixes/15
for period in range (1000,30000,3000):

    sm=2
    x=[]
    y=[]
    esred=[]
    sred=[]
    truesred=[]


    que = collections.deque([],maxlen=period)
    # que2 = collections.deque([],maxlen=period)



    for ugol in range(0,ixes,1):
        sn = math.sin(math.radians(ugol))
        x.append(ugol)
        y.append(sn+sm+ugol/koef)



    count=1
    sum2=0
    # esred
    for iy in y:
        if count<=period:
            sum2+=iy
            # esred.append(None)
            esred.append(sum2 / count)
        else:
            sum2= sum2 - sum2 / period + iy
            esred.append(sum2 / period)
        count+=1




    count=1
    sum2=0
    # sred
    for iy in y:
        if count<=period:
            sum2+=iy
            # sred.append(None)
            sred.append(sum2/count)
            que.append(iy)
        else:
            que.append(iy)
            sum2=sum2-que[0]+iy
            sred.append(sum2/period)
        count+=1


    # # truesred
    # count=1
    #
    # sum2=0
    # for iy in y:
    #     if count<=period:
    #         truesred.append(None)
    #         que2.append(iy)
    #     else:
    #         que2.append(iy)
    #         sum2=sum(que2)
    #         truesred.append(sum2/period)
    #     count+=1




    color = get_color()
    fig = px.line()

    clr = color()
    fig.add_scatter(x=x, y=y, line_color=clr, name='SIN')
    clr = color()
    fig.add_scatter(x=x, y=esred, line_color=clr, name='esred')
    clr = color()
    fig.add_scatter(x=x, y=sred, line_color=clr, name='sred')
    # clr = color()
    # fig.add_scatter(x=x, y=truesred, line_color=clr, name='truesred')

    fig.show()


