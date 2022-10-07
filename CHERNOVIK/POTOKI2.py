import threading

mutex = threading.Lock()
# lock=threading.Lock().acquire()
# unlock=threading.Lock().release()D.update({i:i*1000})

L=[]
D=dict()
NUM = 50000
def apnd ():
    for i in range(NUM):
        L.append(i)

# def apnd ():
#     for i in range(NUM):
#         D.update({i:i*1000})
#


thread1 = threading.Thread(target = apnd)
thread2 = threading.Thread(target = apnd)
thread3 = threading.Thread(target = apnd)
thread4 = threading.Thread(target = apnd)
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()

print(NUM*4,' =  ',len(L))
print(NUM*4,' =  ',len(D))