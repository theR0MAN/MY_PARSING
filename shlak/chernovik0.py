import lzma
import json
import  time

import sys
# https://docs-python.ru/standart-library/modul-lzma-python/funktsija-open-modulja-lzma/




with open ('/home/roman/Рабочий стол/11/10.json', mode='r') as f:
    a =f.read()
    print(sys.getsizeof(a))

timer=time.time()
a = a.encode('utf-8')
print('time encode ',time.time()-timer)


timer=time.time()
a=lzma.compress(a)
print('time compress ',time.time()-timer)
print(sys.getsizeof(a))

with lzma.open("file.xz", "w") as f:
    f.write(a)

with lzma.open("file.xz") as f:
    a = f.read()


timer=time.time()
a=lzma.decompress(a)#.decode('utf-8')
print('time decompress ',time.time()-timer)


timer=time.time()
a=a.decode('utf-8')
print('time decode ',time.time()-timer)


#
# print(' read  ',type(a),a)
#
# a=a.decode('utf-8')
# print(' decode  ',type(a),a)
#
