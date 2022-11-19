# import MetaTrader5 as mt5
import json
from platform import system
import time
import os
# import lzma
import datetime

# dat = datetime.datetime.utcfromtimestamp(int(time.time()))
# year = dat.year
# month = dat.month
# day = dat.day
# hour = dat.hour

hour=0

hourf=23 if hour==0 else hour-1

print(hourf)
# a={"f":1}
#
# if system() == 'Windows':
# 	dL = '\\'
# else:
# 	dL = '/'
#
# putpath = 'G:\\DATA_SBOR\\MOEX'
#
# # get filename
# name = str(hour) + '.json'
#
# nextpath = putpath + dL + str(year)
# if not os.path.exists(nextpath):
# 	os.mkdir(nextpath)
# nextpath = nextpath + dL + str(month)
# if not os.path.exists(nextpath):
# 	os.mkdir(nextpath)
# nextpath = nextpath + dL + str(day)
# if not os.path.exists(nextpath):
# 	os.mkdir(nextpath)
# fullname = nextpath + dL + name
#
# with open(fullname, 'w', encoding='utf-8') as fl:
# 	json.dump(a, fl)