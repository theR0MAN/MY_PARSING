import lzma
import json
import  time

import sys
# https://docs-python.ru/standart-library/modul-lzma-python/funktsija-open-modulja-lzma/

with open ('/home/roman/Рабочий стол/11/10.json', mode='r') as f:
    a =lzma.compress(f.read().encode('utf-8'))

# a=lzma.compress(a)

with lzma.open("/home/roman/Рабочий стол/11/10.roman", "w") as f:
    f.write(a)

with lzma.open("/home/roman/Рабочий стол/11/10.roman") as f:
    a=lzma.decompress(f.read()).decode('utf-8')


# a=lzma.decompress(f.read()).decode('utf-8')

with open("/home/roman/Рабочий стол/11/1000.json",mode='w', encoding='utf-8') as f:
    f.write(a)







#
# print(' read  ',type(a),a)
#
# a=a.decode('utf-8')
# print(' decode  ',type(a),a)
#
