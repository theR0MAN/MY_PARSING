# id = 'sym1 '+ '@' + 'sym2 '+ '@' + 'npersr' + '@' +'nkperso' + '@' + 'nksovh '+ '@' + 'nkoefvih'
# a =id.split('@')
# sym1= a[0]
# sym2= a[1]
# persr= a[2]
# kperso= a[3]
# ksovh=a[4]
# koefvih= a[5]
#
#
# print(sym1)
# print(sym2)
# print(persr)
# print(kperso)
# print(ksovh)
# print(koefvih)


dats = {'Si': ['x1', 'x2', 'x3', 'x4', 'x5']} #,'NGF4*FRTS2'

vectmas={}
for i in dats['Si']:
	vectmas[i]=[]
	for j in dats['Si']:
		if j !=i:
			vectmas[i].append(i+'-'+j)

for sym in vectmas:
	print(sym,vectmas[sym] )