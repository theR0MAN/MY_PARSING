import math
from MAIN.FUNC import *
import plotly.express as px
import collections

# period=680
ixes=50000
koef=ixes/30

keperiod=1

ksin=1
sm=5
for period in range (4000,5000,2000):


    x=[]
    y=[]
    esred=[]
    sred=[]
    coresred=[]
    corsred=[]

    # Resred=[]
    # Rsred=[]



    que = collections.deque([],maxlen=period)
    corque = collections.deque([], maxlen=period)
    # que2 = collections.deque([],maxlen=period)



    for ugol in range(0,ixes,1):
        sn = ksin*math.sin(math.radians(ugol))
        x.append(ugol)
        y.append(sn+sm+ugol/koef)
        # y.append(sn + sm )



    count=1
    sum2=0
    sumr = 0
    # esred
    eperiod=period*keperiod
    for iy in y:
        if count<=eperiod:
            sum2+=iy
            # esred.append(None)
            iesred=sum2 / count
            esred.append(iesred)

            sumr+=iy-iesred
            sredrazn= sumr / count
            # Resred.append(sredrazn)

            coresred.append(iesred + sredrazn)

        else:
            sum2= sum2 - sum2 / eperiod + iy
            iesred = sum2 / eperiod
            esred.append(iesred)

            sumr = sumr - sumr / eperiod + iy-iesred
            sredrazn = sumr / eperiod
            # Resred.append(sredrazn)

            coresred.append(iesred + sredrazn)

        count+=1

# =========================================================================================

    count=1
    sum2=0
    sumr = 0
    # sred
    for iy in y:
        if count<=period:
            sum2+=iy
            # sred.append(None)
            isred = sum2 / count
            sred.append(isred)
            que.append(iy)

            sumr += iy - isred
            sredrazn= sumr / count
            # Rsred.append(sredrazn)

            corque.append(iy - isred)

            corsred.append(isred + sredrazn)


        else:

            sum2 = sum2 - que[0] + iy
            que.append(iy)
            isred = sum2 / period
            sred.append(isred)


            sumr = sumr - corque[0] + iy - isred
            corque.append(iy - isred)
            sredrazn = sumr / period
            # Rsred.append(sredrazn)

            corsred.append(isred + sredrazn)



        count+=1




    color = get_color()
    fig = px.line()

    clr = color()
    fig.add_scatter(x=x, y=y, line_color=clr, name='SIN')

    clr = color()
    fig.add_scatter(x=x, y=esred, line_color=clr, name='esred')
    clr = color()
    fig.add_scatter(x=x, y=sred, line_color=clr, name='sred')

    clr = color()
    fig.add_scatter(x=x, y=coresred, line_color=clr, name='coresred')
    clr = color()
    fig.add_scatter(x=x, y=corsred, line_color=clr, name='corsred')

    # clr = color()
    # fig.add_scatter(x=x, y=Resred, line_color=clr, name='Resred')
    # clr = color()
    # fig.add_scatter(x=x, y=Rsred, line_color=clr, name='Rsred')

    fig.show()