from PROJECT.SBOR.my_lib import *
# from datetime import datetime
# import ntplib
# from time import ctime
# c = ntplib.NTPClient()
# response = c.request('pool.ntp.org')
# t= ctime(response.tx_time)
# print(t)


import datetime
import ntplib

client = ntplib.NTPClient()
response = client.request('pool.ntp.org')
print(datetime.datetime.utcfromtimestamp(response.tx_time) )
# fromtimestamp(response.tx_time))

# print(datetime.fromtimestamp(t))

#
a=myload('watchOrderBookForSymbols')
#
#
#
for type in a:
	for ex in a[type]:
		print(type, ex, a[type][ex]['zadtmstmp'][:50])
		ln=len(a[type][ex]['zadtmstmp'])
		if ln>3:
			print(type, ex,ln,sorted(a[type][ex]['zadtmstmp'])[int(ln/2)],'  ',sum(a[type][ex]['zadtmstmp'])/ln)



# bitmex    bybit   sorted(a[type][ex]['zadtmstmp'][:50])


