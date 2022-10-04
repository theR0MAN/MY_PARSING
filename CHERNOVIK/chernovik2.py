from FUNC import *
import json

getpath = '/media/roman/J/OLDHIST/FONDA'
path2 = '/media/roman/J/jsOLDHIST/FONDA'

start_year = 2020
start_month = 4
start_day = 2
start_hour = 10

stop_year = 2020
stop_month = 4
stop_day = 2
stop_hour = 10

listfiles = getdata(getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
# print(listfiles)

filename=listfiles[0]
# filename=listfiles[0].replace('OLDHIST', 'jsOLDHIST')

if  os.path.exists(filename):
    print('YES')
#
# z=filename.split('/')
# print(z)
#
# yr=z[6]
# mon=z[7]
# dy=z[8]
# name=z[9]
#
# print(yr,"  ",mon,'  ',dy)
#
# nextpath=path2+'/'+ yr
# if not os.path.exists(nextpath):
#     os.mkdir(nextpath)
# nextpath=nextpath+'/' + mon
# if not os.path.exists(nextpath):
#     os.mkdir(nextpath)
# nextpath=nextpath+ '/' + dy
# if not os.path.exists(nextpath):
#     os.mkdir(nextpath)
# fullname = nextpath+'/' +name
#
# with open(fullname,'w') as fl:
#         fl.write('hello')
#
#
# print(fullname)