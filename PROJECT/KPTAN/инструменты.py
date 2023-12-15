import ccxt
# print (ccxt.exchanges)

birza1=ccxt.bybit()
birza2=ccxt.binance()
markets1 = birza1.load_markets()
markets2 = birza2.load_markets()
# instr1=birza1.symbols()
syms=birza2.symbols
print(len(syms))
set1=set()
set2=set()
#
for sym in markets1:
	if':USDT' in sym:
		set1.add(sym)
for sym in markets2:
	if':USDT' in sym:
		set2.add(sym)
setall=set1 & set2
print( set1)
print( set2)
print(setall)


print(len(set1))
print(len(set2))
print(len(setall))
