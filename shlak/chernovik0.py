import multiprocessing
import time
import os
import datetime

def end_func(response):
    print("end_func:",response)




path = '/media/roman/J/Открытие ФОРТС/MQL5/Files/PERkuklfondahistory/'
path2 = '/media/roman/J/OLDHIST/FORTS/'
content = sorted(os.listdir(path), reverse=False)

print(content)

def perepars(i):
    kkk=i
    nm = i.split('.')
    tm = int(nm[0]) * 3600
    dat = datetime.datetime.utcfromtimestamp(tm)
    yr = str(dat.year)
    mon = str(dat.month)
    dy = str(dat.day)
    hr = str(dat.hour)

    if not os.path.exists(path2+yr):
        os.mkdir(path2+yr)
    if not os.path.exists(path2+yr+ '/' + mon):
        os.mkdir(path2+yr+ '/' + mon)
    if not os.path.exists(path2+yr+ '/' + mon+ '/' + dy):
        os.mkdir(path2+yr+ '/' + mon+ '/' + dy)

    name = yr + '/' + mon + '/' + dy + '/' + hr
    filename = name + '.txt'
    # content2.append(name+'.txt')

    file = open(path + i, mode='r', encoding='utf-16')
    zl = file.readlines()
    file.close()
    x = []
    y = []
    b = []
    t0 = 0

    for i in zl:  # пробегаеся по списку строк
        x = i.split()  # дробим каждую строку в элементы списка
        if len(x) > 2:
            if '-' in x[0]:
                x[0] = 'FRTS ' + x[0] + ' s 0'
            else:
                x[0] = 'MOEX ' + x[0] + ' s 0'

            # print(x[2])
            # тут нужно заменить массив стаканов по правилам
            kasks = 0
            kbids = 0
            asks = []
            bids = []
            sasks = []
            sbids = []
            ind = 3
            for u in range(int(x[2])):
                try:
                    if float(x[ind]) > 0:
                        asks.append((x[ind], x[ind + 1]))
                        kasks += 1
                    else:
                        bids.append((str(-float(x[ind])), x[ind + 1]))
                        kbids += 1
                    # print(x[ind],'   ',x[ind+1])
                    ind += 2
                except Exception:
                    print('Error ', x[0], '   ', filename, '   ', nm)
                else:
                    continue
            asks.reverse()

            for i in asks:
                sasks.append(' '.join(i))
            for i in bids:
                sbids.append(' '.join(i))
            y = [x[0]] + [str(kasks)] + sasks + [str(kbids)] + sbids

            t = x.pop(1)
            if t != t0:
                t0 = t
                b.append("\n" + '* ' + t)

        line_data = ' '.join(y)  # переводим в текст список строки
        b.append("\n" + line_data)  # создаем новый массив строк с переходом на новую строку вначале

    zzz = ' '.join(b)  #
    # print(path2 + filename)
    file2 = open(path2 + filename, mode='w', encoding='utf-8')
    file2.write(zzz)
    file2.close()
    print(kkk,'   ',filename)
    return kkk




timer=time.time()
if __name__ == '__main__':
    with multiprocessing.Pool(8) as pool:
        pool.map_async(perepars, content, callback=end_func)
        pool.close()
        pool.join()
print('ALL TIME ', time.time() - timer)

#
# timer=time.time()
# if __name__ == '__main__':
#     pool = multiprocessing.Pool(8)
#     pool.map_async(perepars, content, callback=end_func)
#     pool.close()
#     pool.join()
# print('ALL TIME ', time.time() - timer)