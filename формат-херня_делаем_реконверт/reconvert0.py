
import plotly.express as px
import lzma
import json

name='/media/roman/J/rOLDHIST/FORTSALL/2021/11/22/19.roman'
# name='/media/roman/J/rOLDHIST/FONDA/2020/5/12/14.roman'
lz=lzma
with lz.open(name) as f:
    a=dict(json.loads(lz.decompress(f.read()).decode('utf-8')))

set1=set()
K1=0
# получим первый ключ
for timekey in a:
    K1=timekey
    for dicts in a[timekey]:# a[key] - list dicts
        set1.add(dicts['i'])
    break
#print Нужно перекинуть вначалo инструменты, которые изменились по ходу.
for timekey in a:
    for dct in a[timekey]:# a[key] - list dicts
        if dct['i'] not in set1:
            # print(timekey,"   ",dicts['i'],"  ", dicts)
            a[K1].append(dct)
        set1.add(dict['i'])

#  преобразуем в человеческую структуру г

#d1 список инструментов по первому ключу - формируем словарь списков

s0=set()
s1=set()

d1=dict()
d2=dict()
for timekey in a:
    for dct in a[timekey]:
        name = dct['i'] + '*' + dct['p']
        d2[name] = []
        s0.add(name)
    break

# for i in d2:
#     print(i,d2[i])


for timekey in a:
    s1=set()
    for dct in a[timekey]:
        d1 = dict()
        for key in dct:
            if key!="i" and key!="p":
                d1[key]=dct[key]
        name = dct['i'] + '*' + dct['p']
        if name not in s1:
            s1.add(name)
            try:
                d2[name].append(d1)
            except:
                print(' произошла собачья хрень')
                d2[name]=[]
                d2[name].append(d1)
    # если в следующем списке по временному ключу нет инструмента, т. е он повторяется (не пишется), то добавляем флаг повтора 'F':'r'
    # s2 если рынок закрыт - то 'F':'с'.
    s2=s0.difference(s1)
    for i in s2:
        d2[i].append(['r'])



file2 = open('1.txt', mode='w', encoding='utf-8')
for i in d2:
    file2.write(i+"   "+str(d2[i]))
file2.close()

file2 = open('0.txt', mode='w', encoding='utf-8')
for i in a:
    file2.write(i+"   "+str(a[i]))
file2.close()

