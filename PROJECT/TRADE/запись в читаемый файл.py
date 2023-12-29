import time
file1 = open("test.txt", "a+")
# работа с файлом
while True:
	time.sleep(1)
	a=file1.read()
	file1.seek(0)
	print(a)
# file1.close()