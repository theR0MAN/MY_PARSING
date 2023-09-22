
class A:
	b=11

	def hello(x):
		print('HELLO!!',x)



A.hello(11)


c=A
print(c)
print(A)

c=A ()
print(c)
print(A)

c.hello()

