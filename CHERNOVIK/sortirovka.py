import time
from random import randint


T1=list(i for i in range(1000000))
T2=list(i for i in range(1000000,0,-1))

a = []
for i in range(1000000):
    a.append(randint(1, 99))


t1=time.time()
z=sorted(T1)
t2=time.time()
print(' t1 ',t2-t1)

t1=time.time()
z=sorted(T1)
t2=time.time()
print(' t1 ',t2-t1)
t1=time.time()
z=sorted(T1)
t2=time.time()
print(' t1 ',t2-t1)

t1=time.time()
z=sorted(T2)
t2=time.time()
print('t2 rev ',t2-t1)
t1=time.time()
z=sorted(T2)
t2=time.time()
print('t2 rev ',t2-t1)
t1=time.time()
T2.sort()
t2=time.time()
print('t2.sort() rev ',t2-t1)

t1=time.time()
z=sorted(a)
t2=time.time()
print('random ',t2-t1)
t1=time.time()
z=sorted(a)
t2=time.time()
print('random ',t2-t1)
t1=time.time()
z=sorted(a)
t2=time.time()
print('random ',t2-t1)
print()

t1=time.time()
for i in T1:
    if i>0:
        a=2
t2=time.time()
print('cicle ',t2-t1)
# 1 комит
# 1 после мержа
# 1 после мержа 2