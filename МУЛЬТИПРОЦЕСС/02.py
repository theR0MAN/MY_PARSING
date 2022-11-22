# Chapter06/example1.py
from threading import Thread
from multiprocessing import Process
import time

class Cnt:
    def __int__(self):
        self.a=2


    def st(self):
        self.calpr()

    def count_down(self,a, s):
        print(f'Process 2 {a} starting...')
        c=a**s
        print(a," finish  ")

    def calpr(self):


        Thread(target=self.count_down, args=(100, 4000000)).start()
        process2 = Thread(target=self.count_down, args=(50,  4000000))
        process3 = Thread(target=self.count_down, args=(40, 4000000))
        process4 = Thread(target=self.count_down, args=(30, 4000000))


        process2.start()
        process3.start()
        process4.start()


        process2.join()
        process3.join()
        process4.join()
        print('Done.')




FF=Cnt()

FF.calpr()






