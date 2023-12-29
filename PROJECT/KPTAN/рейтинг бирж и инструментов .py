
from PROJECT.my_lib import *
import  time
minpovtinst=30  #  убрать инструменты, которые повторяются меньше чем на minpovtinst рынках
minkinstbirz=40   # убрать биржи, на которых оставшихся инструментов меньше  minkinstbirz
topsyms=50# оставить в итоге символы из топа в количестве не более  topsyms

def func_sort (a,spi):
	rez=[]
	for kr in a:
		for insr in spi:
			z = insr.partition('/')[0]
			if z== kr:
				rez.append(insr)
	return  rez

setopt=set()
data= myload('Kriptoinf.roman')
# print(data['gateio'])
print(time.time())
# quit()
couninst=dict()
rezdat=dict()
for ex in data:
	rezdat[ex]=[]
	for sym in data[ex]:
		if '/USDT' in sym and ('-C'  in sym or'-P'  in sym) and data[ex][sym]['active'] == True:
			setopt.add(ex)

		if '/USDT' in sym and '-C'not in sym and '-P'not in sym and data[ex][sym]['active']==True:
			rezdat[ex].append(sym)
			a=sym.partition('/')[0]
			if a in couninst:
				couninst[a]+=1
			else:
				couninst[a]=1
symset=set()
couninstrez=dict()
for sym in couninst:
	if couninst[sym]>=minpovtinst:
		couninstrez [sym]= couninst[sym]
		symset.add(sym)
couninstrez=mysortdict(couninstrez)
#
count=0
couninstreztopset=set()
for sym in couninstrez:
	count+=1
	if  count>topsyms:
		break
	else:
		couninstreztopset.add(sym)



rezdat=dict()
for ex in data:
	rezdat[ex]=[]
	for sym in data[ex]:
		if '/USDT' in sym and '-C'not in sym and '-P'not in sym and data[ex][sym]['active']==True:
			a=sym.partition('/')[0]
			if a in couninstreztopset:
				rezdat[ex].append(sym)
	if len(rezdat[ex])<minkinstbirz:
		del rezdat[ex]

rb=dict()
for ex in rezdat:
	rb[ex]=len(rezdat[ex])
rb=mysortdict(rb)

itog=dict()
for ex in rb:
	itog[ex] =func_sort (couninstrez,rezdat[ex])
countfut=dict()
for ex in itog:
	countfut[ex]=0
	for sym in itog[ex]:
		if ":USDT" in sym:
			countfut[ex]+=1
	if countfut[ex]==0:
		del countfut[ex]
countfut=mysortdict(countfut)
countspot=dict()
for ex in itog:
	countspot[ex]=0
	for sym in itog[ex]:
		if ":USDT" not in sym:
			countspot[ex]+=1
		else:
			del countspot[ex]
			break
	if ex in countspot:
		if countspot[ex] == 0:
			del countspot[ex]
countspot=mysortdict(countspot)

print('kvo birz ',len(data))
# рейтинг символов
print(len(couninstrez),couninstrez)
# рейтинг бирж
print('all exc',len(rb),rb)
# рейтинг бирж по фьючам
print('futures ',len(countfut),countfut)
# рейтинг бирж onlyspot
print('onlyspot',len(countspot),countspot)
print("option markets  ",setopt)

myput("Frez",itog)
# ITOG
for ex in itog:
	print(ex, itog[ex])




