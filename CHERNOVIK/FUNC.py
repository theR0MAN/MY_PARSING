import os
from platform import system
def getdata(getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour):
    '''
    возвращает список путей к файлам
    :param getpath:
    :param start_year:
    :param start_month:
    :param start_day:
    :param start_hour:
    :param stop_year:
    :param stop_month:
    :param stop_day:
    :param stop_hour:
    :return: list
    '''
    if system()=='Windows':
        dL='\\'
    else:
        dL='/'
    if stop_year < start_year \
            or stop_year == start_year and stop_month < start_month \
            or stop_year == start_year and stop_month == start_month and stop_day < start_day \
            or stop_year == start_year and stop_month == start_month and stop_day == start_day and stop_hour < start_hour:
        print("  ошибка введенный конец периода начинается раньше его начала ")
        quit()
    if start_month > 12 or stop_month > 12 or start_day > 31 or stop_day > 31 or start_hour > 23 or stop_hour > 23:
        print(" Ошибка - введено хреновое время")
        quit()
    if start_month <= 0 or stop_month <= 0 or start_day <= 0 or stop_day <= 0 or start_hour < 0 or stop_hour < 0:
        print("Ошибка - введено отрицательное время")
        quit()

    listfiles = []
    flag = False
    for y in range(start_year, stop_year + 1):
        if flag:
            break
        for m in range(start_month, 13):
            if flag:
                break
            for d in range(start_day, 32):
                if flag:
                    break
                for h in range(start_hour, 24):
                    if os.path.exists(getpath + dL + str(y) + dL + str(m) + dL + str(d) + dL + str(h) + '.txt'):
                        listfiles.append(getpath + dL + str(y) + dL + str(m) + dL + str(d) + dL + str(h) + '.txt')
                    if y >= stop_year and m >= stop_month and d >= stop_day and h >= stop_hour:
                        flag = True
                        break
                start_hour = 0
            start_day = 1
        start_month = 1
    return listfiles
