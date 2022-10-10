
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

for key in a:
    for instr in a[key]:
        if(instr['i']=='SBER'):

            x.append(k)
            y1.append(instr['a'])
            y2.append(instr['b'])
            k+=1
#
# t=[1, 2,3]
print('start')
fig = px.line(width=3840*8,height=2160*2)
fig.add_scatter(x=x, y=y1, line_color='red')
fig.add_scatter(x=x, y=y2, line_color='blue')
fig.show()
