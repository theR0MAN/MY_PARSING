import psutil

# p = psutil.Process()
# print(p.connections(kind='inet') )

# print(psutil.net_connections(kind='inet') )

p=psutil.net_connections(kind='inet')

# for k in p :
# 	print(k)

print(len(p))