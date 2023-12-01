import os
import time
import datetime
putpath = 'G:\\DATA_SBOR\\'
# mymarkets = ['FRTS2', 'MOEX2', 'USAFUT', 'CUR', 'CURcross']
# for name in mymarkets:
# 	if not os.path.exists(putpath + name):
# 		os.mkdir(putpath + name)


dat = datetime.datetime.utcfromtimestamp(int(time.time()))
year = str(dat.year)
month=str(dat.month)
day = str(dat.day)


name=year+'-'+month+'-'+day
print(name)
