import time
import datetime

z="G:\\DATA_SBOR\\KRIPTA\\binance\\2024\\1\\1\\11abm.roman"
x = z.split('\\')
l = len(x)
year = int(x[l - 4])
print(year)
mon = int(x[l - 3])
print(mon)
day = int(x[l - 2])
print(day)
hr = int(x[l - 1].split('.')[0][:2])
print(hr)
tm = int(time.mktime(datetime.datetime(year, mon, day, hr).timetuple()))
