
import plotly.express as px
import lzma
import json

name='/media/roman/J/rOLDHIST/FONDA/2020/5/12/14.roman'
lz=lzma
with lz.open(name) as f:
    a=dict(json.loads(lz.decompress(f.read()).decode('utf-8')))

# print(a["1588672803"])
k=0
x=[]
y1=[]
y2=[]
y3=[]

for key in a:
    for instr in a[key]:
        if(instr['i']=='SBER'):

            x.append(k)
            y1.append(instr['a'])
            y2.append(instr['b'])
            y3.append(instr['l'])
            k+=1
#
# t=[1, 2,3]
print('start')
fig = px.line(width=3840*2,height=2160)
fig.add_scatter(x=x, y=y1, line_color='red',name ='ask')
fig.add_scatter(x=x, y=y2, line_color='blue',name ='bid')
fig.add_scatter(x=x, y=y3, line_color='green',name ='last')
fig.show()

