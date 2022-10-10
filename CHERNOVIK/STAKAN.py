
import plotly.express as px
import lzma
import json

name='/media/roman/J/rOLDHIST/FONDA/2020/5/12/14.roman'
lz=lzma
with lz.open(name) as f:
    a=dict(json.loads(lz.decompress(f.read()).decode('utf-8')))

# print(a["1588672803"])
k=1
x=[]
y1=[]
y2=[]

price=[]
vol=[]
type=[]


for key in a:
    for i in a[key]:
        if(i['i']== 'MGNT'):
            # global n
            n=0
            for c,v in i['asks']:
                price.append(c)
                if v>0 and v<10:
                    v2=2
                elif v>9 and v<100:
                    v2 = 4
                elif v>99 and v<1000:
                    v2 = 8
                elif v>999 and v<10000:
                    v2 = 16
                elif v > 9999:
                    v2 = 32
                vol.append(v2)
                x.append(k)
                type.append('ask')
                # n+=1
                # if n>5:
                #     break

            n=0
            for c, v in i['bids']:
                price.append(c)
                if v>0 and v<10:
                    v2=2
                elif v>9 and v<100:
                    v2 = 4
                elif v>99 and v<1000:
                    v2 = 8
                elif v>999 and v<10000:
                    v2 = 16
                elif v > 9999:
                    v2 = 32
                vol.append(v2)
                x.append(k)
                type.append('bid')
                # n+=1
                # if n>5:
                #     break

            k += 1
            # if k>50:
            #     break
            # x.append(k)
            # y1.append(i['a'])
            # y2.append(i['b'])
            # k+=1
#
# t=[1, 2,3]
print('start')
# fig = px.line(width=3840*4,height=2160*2)
# fig.add_scatter(x=x, y=y1, line_color='red')
# fig.add_scatter(x=x, y=y2, line_color='blue')
# fig.show()



fig = px.scatter(
                 x=x, y=price,
                 color=type,
                 size=vol
                   ,width=3840,height=2160
                 )



fig.show()