
a={"1":10,"2":11,"3":21,"7":45,"8":4,"9":133}
print(a)


def find_key(dct,key):
	if key in dct:
		return key
	else:
		for i in range(int(key)-1,0,-1):
			if str(i) in dct:
				return str(i)


print(find_key(a,"11"))