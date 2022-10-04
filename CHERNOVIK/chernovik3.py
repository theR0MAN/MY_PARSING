asks= [('446.79', '30.0'), ('446.86', '46.0'), ('446.88', '67.0'), ('446.89', '5.0'), ('446.92', '19.0'), ('446.93', '100.0')]
y=[]
for i in asks:
    print(i)
    y.append(' '.join(i))

x = ' '.join(y)
print(y)
print(x)

s=[1,2,3]
v=[2,3,4]
z=s+[12]+v
print(z)

b=str(-float('-10'))
print(b)

# timer=time.time()
# with py7zr.SevenZipFile("/home/roman/Рабочий стол/11/10.7z", 'w') as archive:
#     archive.writeall("/home/roman/Рабочий стол/11/10.json")
# print('PACKING time ',time.time()-timer)

# распаковка файла 10 в файл yes.json
# timer=time.time()
# with py7zr.SevenZipFile("/home/roman/Рабочий стол/11/10", 'a') as archive:
#     archive.write("/home/roman/Рабочий стол/11/yes.json")
# print('UNPACKING time ',time.time()-timer)
#
# with py7zr.SevenZipFile("/home/roman/Рабочий стол/11/10.7z", 'r') as archive:
#     archive.extractall(path="/home/roman/Рабочий стол/11/101.json")
