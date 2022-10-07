# https://docs-python.ru/standart-library/paket-multiprocessing-python/proksi-obekty-menedzhera-modulja-multiprocessing/
import multiprocessing
# manager = multiprocessing.Manager()
# D = manager.dict({})

# manager = multiprocessing.Manager()
D = multiprocessing.Manager().dict({})

D.update({'yes':30})
print(D)
print(type(D))
def end_func(response):
    print("end_func:", response)

def fun(i):
    D.update({i:i*1000})
    return str(i)+" OK"

content=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]

if __name__ == '__main__':
    with multiprocessing.Pool(9) as pool:
        pool.map_async(fun, content, callback=end_func)
        pool.close()
        pool.join()

print(D)