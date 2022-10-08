# # SuperFastPython.com
# # example of starting a child process only in __main__
# from multiprocessing import Process
#
#
# # function executed in a new process
# def task():
# 	print('Hello from a child process', flush=True)
#
#
# # check for top-level environment
# if __name__ == '__main__':
# 	# create and configure a new process
# 	process = Process(target=task)
# 	# start the new process
# 	process.start()
# 	# wait for the new process to finish
# 	process.join()

import multiprocessing
#
# def worker(q):
#     q.put('X' * 10000)
#
# if __name__ == '__main__':
#     queue = multiprocessing.Queue()
#     p = multiprocessing.Process(target=worker, args=(queue,))
#     p.start()
#     p.join()    # это тупик
#     obj = queue.get()

# from multiprocessing import Pool
#
# def worker(x):
#     return x*x
# if __name__ == '__main__':
#     # запускаем 4 рабочих процесса
#     with Pool(processes=4) as pool:
#         it = pool.imap(worker, range(10))
#         # использование встроенной функции next()
#         print(next(it))    # выведет 0
#         print(next(it))    # выведет 1
#         # использование метода-итератора с аргументом `timeout`
#         # выведет "4" если компьютер не очень медленный
#         print(it.next(timeout=1))

import multiprocessing
# manager = multiprocessing.Manager()
# D = manager.dict({})
# D.update({'yes':30})
# print(D)
# print(type(D))
def end_func(response):
    print("end_func:", response)

def fun(i):
    # D.update({i:i*1000})
    return str(i)+" OK"

content=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]

if __name__ == '__main__':
    with multiprocessing.Pool(9) as pool:
        pool.map_async(fun, content, callback=end_func)
        pool.close()
        pool.join()

