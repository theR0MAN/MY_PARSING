import os
import py7zr
# https://pypi.org/project/py7zr/
import numpy


# https://habr.com/ru/company/selectel/blog/547290/
# print(os.path.exists('/media/roman/J/Открытие ФОРТС'))
# print(os.listdir("/media/roman/J/Открытие ФОРТС"))
# if not os.path.exists('test_dir'):
#     os.mkdir('test_dir')



# with py7zr.SevenZipFile('target.7z', 'w') as z:
#     z.writeall('./base_dir')
#

# text_file = open('/media/roman/J/Открытие ФОРТС/MQL5/Files/PERkuklfondahistoryall/452733.txt', mode='r',encoding='utf-16')
# lines = text_file.read().split()
# print (lines)
# text_file.close()


# zl = text_file.readlines()
# zl2 = zl.split(' ')


# print(zl)

# for i in zl:
#     print(i)
#


text_file = open('/home/roman/MY_PARSING/files/452725.txt', mode='r',encoding='utf-16')
zl = text_file.read()
file2 = open('/home/roman/MY_PARSING/files/REC.txt', mode='w', encoding='utf-8')
file2.write(zl)
text_file.close()
file2.close()
# print(zl2)
#
# x=0
# for i in zl2:
#     if '\n' in i:
#         print(i)
#         x+=1
# print(x)
