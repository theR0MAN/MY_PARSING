# Chapter06/example1.py

from multiprocessing import Process
import time


def count_down(a, s):
    print(f'Process 2 {a} starting...')
    c=a**s
    print(a," finish  ")

if __name__ == '__main__':
    process1 = Process(target=count_down, args=(100, 4000000))
    process2 = Process(target=count_down, args=(50,  4000000))
    process3 = Process(target=count_down, args=(40, 4000000))
    process4 = Process(target=count_down, args=(30, 4000000))
    process5 = Process(target=count_down, args=(60, 500000))
    process6 = Process(target=count_down, args=(70,  4000000))
    process7 = Process(target=count_down, args=(80, 4000000))
    process8 = Process(target=count_down, args=(90, 4000000))
    process9 = Process(target=count_down, args=(99, 4000000))
    process10 = Process(target=count_down, args=(77, 4000000))

    process1.start()
    process2.start()
    process3.start()
    process4.start()
    process5.start()
    process6.start()
    process7.start()
    process8.start()
    process9.start()
    process10.start()

    process1.join()
    process2.join()
    process3.join()
    process4.join()
    process5.join()
    process6.join()
    process7.join()
    process8.join()
    process9.join()
    process10.join()

    print('Done.')