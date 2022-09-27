import os
import time
import datetime



path='/media/roman/J/Открытие ФОРТС/MQL5/Files/PERkuklfondahistoryall'

content = sorted(os.listdir(path),reverse=False)
content2=[]
for i in content:
    nm=i.split('.')
    tm=int(nm[0])*3600
    dat=datetime.datetime.utcfromtimestamp(tm)
    yr=str(dat.year)
    mon=str(dat.month)
    dy=str(dat.day)
    hr=str(dat.hour)
    name=yr+'_'+mon+'_'+dy+'_'+hr
    content2.append(name+'.txt')
    # print(f'  {name}' )

print(content)
print(content2)
