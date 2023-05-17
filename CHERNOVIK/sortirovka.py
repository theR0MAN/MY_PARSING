
from platform import system
# from multiprocessing import Process
from threading import Thread
import time
import os
import lzma
import datetime
dat = datetime.datetime.utcfromtimestamp(int(time.time()))
timekey = str(dat.minute * 60 + dat.second)
print(dat.minute)