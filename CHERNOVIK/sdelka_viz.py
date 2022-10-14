
import plotly.express as px
import lzma
import json

name='/media/roman/J/rOLDHIST/FONDA/2020/5/12/14.roman'
lz=lzma
with lz.open(name) as f:
    b1=dict(json.loads(lz.decompress(f.read()).decode('utf-8')))

name='/media/roman/J/rOLDHIST/FONDA/2020/5/12/15.roman'
lz=lzma
with lz.open(name) as f:
    b2=dict(json.loads(lz.decompress(f.read()).decode('utf-8')))

name='/media/roman/J/rOLDHIST/FONDA/2020/5/12/16.roman'
lz=lzma
with lz.open(name) as f:
    b3=dict(json.loads(lz.decompress(f.read()).decode('utf-8')))
name='/media/roman/J/rOLDHIST/FONDA/2020/5/12/17.roman'
lz=lzma
with lz.open(name) as f:
    b4=dict(json.loads(lz.decompress(f.read()).decode('utf-8')))

a=b1|b2|b3|b4
# print(a["1588672803"])
k=0
x=[]
y1=[]
y2=[]
seti=set()

for key in a:
    for instr in a[key]:
        seti.add(instr['i'])
        if(instr['i']=='IRAO'):


            x.append(k)
            y1.append(instr['a'])
            y2.append(instr['b'])
            k+=1
#
# t=[1, 2,3]
print('start')
fig = px.line(width=len(x),height=2160*2)
fig.add_scatter(x=x, y=y1, line_color='red')
fig.add_scatter(x=x, y=y2, line_color='blue')
fig.show()
print(seti)

