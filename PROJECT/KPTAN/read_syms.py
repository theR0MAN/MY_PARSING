# import  ccxt
# import os ,datetime
# import time
# import operator

from PROJECT.SBOR.my_lib import *



# name='G:\\DATA_SBOR\\ASYMBOLS_INFO\\2023\\12\\13-Kripto.roman'
namemain='G:\\DATA_SBOR\\ASYMBOLS_INFO\\2023\\12\\14-Kriptoinf.roman'



# datasmall = myload(name)
data= myload(namemain)

# print(data['bybit']['BTC/USDT'])
# quit()
symset=set()
for sym in data['bybit']:
	if '/USDT:USDT' in sym and '-C'not in sym and '-P'not in sym and data['bybit'][sym]['active']==True:  
		symset.add(sym.partition('/')[0])
print(len(symset), symset) #,syyms
# quit()
rezdat=dict()
for ex in data:
	rezdat[ex]=[]
	for sym in data[ex]:
		if '/USDT' in sym and '-C'not in sym and '-P'not in sym and data[ex][sym]['active']==True:
			a=sym.partition('/')[0]
			if a in symset:
				rezdat[ex].append(sym)
	if len(rezdat[ex])==0:
		del rezdat[ex]
myput('Frez',rezdat)

rezdat=myload('Frez')
# print(rezdat)


cl=0
for ex in rezdat:
	ln=len(rezdat[ex])
	cl+=ln
	print(ex,'  ',ln)
print(cl)
# print(rezdat)

countdict=dict()
for sims in symset:
	countdict[sims]=0


for ex in rezdat:
	for sym in rezdat[ex]:
		a = sym.partition('/')[0]
		if a in symset:
			countdict[a]+=1



countdict=mysortdict(countdict)
# countdict = dict(sorted(countdict.items(), reverse=True))
print("  CRYPTOS:")
for key in countdict:
	print( key,"  ",countdict[key])

# for ex in rezdat:
# 	for sym in rezdat[ex]:
# 		if sym=='BTC/USDT':
# 			print(ex)
# 			break



