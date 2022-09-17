
a=['2','2','4','5','6']

b=a.copy()
c=list(0 for i in range(10))
k=0
for i in a:
    b[k]=float(i)
    k+=1

print(b)
print(c)


