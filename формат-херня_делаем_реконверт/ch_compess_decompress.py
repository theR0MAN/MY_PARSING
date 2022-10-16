from MAIN.FUNC import *
import json
import multiprocessing
import time
import os
import lzma
import datetime

name='/media/roman/J/jsOLDHIST/FORTSALL/2021/11/22/19.json'
lz=lzma
with open(name, mode='r') as f:
    a = dict(json.load(f))

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

    s2=s0.difference(s1)
    for i in s2:
        d2[i].append(['r'])




file2 = open('100.txt', mode='w', encoding='utf-8')
for i in d2:
    file2.write(i+"   "+str(d2[i]))
file2.close()

a=lzma.compress(json.dumps(d2).encode('utf-8'))

with lz.open('100.roman', "w") as f:
    f.write(a)

with lz.open('100.roman') as f:
    a=dict(json.loads(lz.decompress(f.read()).decode('utf-8')))

print(a)