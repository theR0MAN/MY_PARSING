import time
import datetime

dat = datetime.datetime.utcfromtimestamp(int(time.time()))
minsec = str(dat.minute * 60 + dat.second)

print(f'minsec={minsec}  dat.year={dat.year}  dat.month={dat.month}  dat.day={dat.day}  dat.hour={dat.hour}   dat.minute={dat.minute} dat.second={dat.second}  ' )

print(type(dat.hour))

a = dict()
data = dict()
print(len(a))