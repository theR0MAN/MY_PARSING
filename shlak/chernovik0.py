import sqlite3 as sl

c=dict()
a={'q':1,'g':2,'d':4}
b={'q1':1,'g1':2,'d1':4}

y=a|b
a|=b
c|=b

print(y)
print(a)

print(c)