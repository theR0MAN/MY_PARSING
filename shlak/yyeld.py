

a=[5,4,3,6,9,8,11]

def F(it):
	for i in it :
		for i in range(5):
			yield i*2


z=F(a)

while True:
	try:
		print(next(z))



	except:
		print('stop')
		break

for i in range(10):
	print(i)
