from PROJECT.SBOR.my_lib import *
# from datetime import datetime
# import ntplib
# from time import ctime
# c = ntplib.NTPClient()
# response = c.request('pool.ntp.org')
# t= ctime(response.tx_time)
# print(t)
import os

# pth='G:\\NEWKRIPT'
#
# dr= os.listdir(pth)
# print(dr)

# поиск папок в папке=поиск каталогов в каталоге
# import os
# pth = 'G:\\NEWKRIPT'
# folders = [e for e in os.listdir(pth) if os.path.isdir(e)]
# print(folders)
a=myload('z')

for key in a:
	print(key,mysortdict(a[key]))





