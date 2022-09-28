import multiprocessing
import  time
def end_func(response):
    print("end_func:",response)


def out(x,y,z):
    print(f"value: {x}  {y}  {z}")
    ppo=5000 ** 1000000
    return x,y,z,x+y+z
param=[(1,2,3),(4,5,6),(7,8,9),(10,11,12),(13,14,15),(16,17,18),(19,20,21),(22,23,24)]# x,y,z
timer=time.time()
if __name__=='__main__':
    with multiprocessing.Pool(8) as p:
        p.starmap_async(out,param,callback=end_func)
        p.close()
        p.join()


print('ALL TIME ' , time.time()-timer)
# print(5000**100000)