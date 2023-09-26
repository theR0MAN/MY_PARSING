# зачача -распараллелить распаковку, синх мап  , распаковывать порциями - чтобы оперативы  хватило, но
# не больше чем ядер за раз
# а потом скармливать по одному в общее тело - для  тестера понадобится
from multiprocessing import Pool
from PROJECT.TEST.Test_lib import getdata_merge, gettm
from Viz_lib import get_color
from platform import system
import plotly.express as px
import lzma
import json
import time
import datetime
from numba import njit


# while True:
# 	dat = datetime.datetime.utcfromtimestamp(int(time.time()))
# 	time.sleep(1)
# 	print(dat.second)

for i in range(10):
	i=str(i)
	print(i+'m')