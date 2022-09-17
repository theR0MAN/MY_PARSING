from itertools import product
import numpy as np
from collections import deque

a=[4,5,6,(6,3,7,[11,2,3,5,4,3,55,6],2)]
print(a[3][3])

for i in a[3][3]:
    print(i)


a=[i for i in range(20, 100, 2)]
print(a)

start=1
stop=10
num=20

a,b=np.linspace(start, stop, num, endpoint=True, retstep=True, dtype=float)

print(a)

for i in a:
    print(i)
print(b)

list_a = [1, 2020, 70]
list_b = [2, 4, 7, 2000]
list_c = [3, 70, 7]



print('NEXT')
for a, b, c in product(list_a, list_b, list_c):
    print(f'a={a}   b={b}  c={c}')

for a, b, c in product([5], [4], [8]):
    print(f'a={a}   b={b}  c={c}')

print('UNPACK')
LIST=(list_a,list_b,list_c)
par= (a,b,c)
for par in product(*LIST):
    print(f'a={par[0]}   b={par[1]}  c={par[2]}')
print('STOP UNPACK')



print('stop')
