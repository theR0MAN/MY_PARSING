from numba import njit
import numpy as np
import time

K=50000000

a=[]
b=[]


timer =time.time()
for i in range (K):
	a.append(i)
	b.append(i)
print(f" создание массивов  {time.time()-timer}")
# print(a)
# print(b)

timer =time.time()
na=np.array(a)
nb=np.array(b)
print(f" преобразование масив нумпай  {time.time()-timer}")
# print(na)
# print(nb)

timer =time.time()
c=[]
ln=len(a)
for i in range(ln):
	c.append(a[i]+b[i])
print(f" easy count  {time.time()-timer}")
# print(c)

timer =time.time()
c= np.zeros(len(a))
ln=len(a)
for i in range(ln):
	c[i]=a[i]+b[i]
print(f" easy count NUMPY {time.time()-timer}")
# print(c)

timer =time.time()
# c2= np.zeros(len(a))
c=na+nb
print(f" VECTORIZE  {time.time()-timer}")
# print(na)
# print(nb)
# print(c)


# def sm (m1,m2):
# 	c=[]
# 	ln = len(m1)
# 	for i in range(ln):
# 		c.append(m1[i] + m2[i])
# 	return c
#
# @njit
# def smj (m1,m2):
# 	c=[]
# 	ln = len(m1)
# 	for i in range(ln):
# 		c.append(m1[i] + m2[i])
# 	return c


# timer =time.time()
# sm(a,b)
# print(f" easy FUNC count  {time.time()-timer}")
#
# timer =time.time()
# smj(na,nb)
# print(f" easy NJIT FUNC count  {time.time()-timer}")
#
# #
# @njit
# def f(n):
#     s = 0.
#     for i in range(n):
#         s += sqrt(i)
#     return s