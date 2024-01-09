import psutil
p=psutil.net_connections(kind='inet')
# for k in p :
# 	print(k)
print(len(p))