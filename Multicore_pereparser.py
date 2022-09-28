import multiprocessing
import time
import os
import time
import datetime

path = '/media/roman/J/Открытие ФОРТС/MQL5/Files/PERkuklfondahistoryall'
path2 = '/media/roman/J/OLDHIST/FORTSALL/'

content = sorted(os.listdir(path), reverse=False)
content2 = []
for i in content:
    nm = i.split('.')
    tm = int(nm[0]) * 3600
    dat = datetime.datetime.utcfromtimestamp(tm)
    yr = str(dat.year)
    mon = str(dat.month)
    dy = str(dat.day)
    hr = str(dat.hour)
    name = yr + '_' + mon + '_' + dy + '_' + hr
    filename = name + '.txt'
    # content2.append(name+'.txt')

    file = open(path + '/' + i, mode='r', encoding='utf-16')
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
                if float(x[ind]) > 0:
                    asks.append((x[ind], x[ind + 1]))
                    kasks += 1
                else:
                    bids.append((str(-float(x[ind])), x[ind + 1]))
                    kbids += 1
                # print(x[ind],'   ',x[ind+1])
                ind += 2
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

    file2 = open(path2 + filename, mode='w', encoding='utf-8')
    file2.write(zzz)
    file2.close()
    print(filename)

