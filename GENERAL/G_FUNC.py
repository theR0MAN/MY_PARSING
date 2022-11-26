import os
from platform import system
import random

def get_color():
    i = -1
    def func():
        colors = ['black', 'red', 'blue', 'brown', 'green', 'violet', 'yellow', 'maroon', 'gold', 'pink', 'silver',
                   'coral', 'chocolate']
        colors0 = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure',
                   'beige', 'bisque', 'black', 'blanchedalmond', 'blue',
                   'blueviolet', 'brown', 'burlywood', 'cadetblue',
                   'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
                   'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan',
                   'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen',
                   'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange',
                   'darkorchid', 'darkred', 'darksalmon', 'darkseagreen',
                   'darkslateblue', 'darkslategray', 'darkslategrey',
                   'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue',
                   'dimgray', 'dimgrey', 'dodgerblue', 'firebrick',
                   'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro',
                   'ghostwhite', 'gold', 'goldenrod', 'gray', 'grey', 'green',
                   'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo',
                   'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen',
                   'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan',
                   'lightgoldenrodyellow', 'lightgray', 'lightgrey',
                   'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen',
                   'lightskyblue', 'lightslategray', 'lightslategrey',
                   'lightsteelblue', 'lightyellow', 'lime', 'limegreen',
                   'linen', 'magenta', 'maroon', 'mediumaquamarine',
                   'mediumblue', 'mediumorchid', 'mediumpurple',
                   'mediumseagreen', 'mediumslateblue', 'mediumspringgreen',
                   'mediumturquoise', 'mediumvioletred', 'midnightblue',
                   'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy',
                   'oldlace', 'olive', 'olivedrab', 'orange', 'orangered',
                   'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise',
                   'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink',
                   'plum', 'powderblue', 'purple', 'red', 'rosybrown',
                   'royalblue', 'rebeccapurple', 'saddlebrown', 'salmon',
                   'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver',
                   'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow',
                   'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato',
                   'turquoise', 'violet', 'wheat', 'white', 'whitesmoke',
                   'yellow', 'yellowgreen']
        nonlocal i
        i += 1
        if i<13:
            return colors[i]
        else:
            return random.choice(colors0)
    return func


def getdata_merge(onlymerge,minutki,markets,getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour):

    fln = '_mnt.roman' if minutki else '.roman'
    dL = '\\' if system() == 'Windows' else '/'

    getpath = getpath +dL+ markets[0]
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
    global name
    listfiles = []
    flag = False
    for y in range(start_year, stop_year + 1):
        name1 = getpath + dL + str(y)
        if flag:
            break
        if not os.path.exists(name1):
            continue
        for m in range(start_month, 13):
            name2 = name1 + dL + str(m)
            if flag:
                break
            if not os.path.exists(name2):
                continue
            for d in range(start_day, 32):
                name3 = name2 + dL + str(d)
                if flag:
                    break
                if not os.path.exists(name3):
                    continue
                for h in range(start_hour, 24):
                    name10 = name3 + dL + str(h) + fln


                    if os.path.exists(name10):
                        listfiles.append(name10)

                    if y > stop_year or \
                            y == stop_year and m > stop_month or \
                            y == stop_year and m == stop_month and d > stop_day or \
                            y == stop_year and m == stop_month and d == stop_day and h >= stop_hour:
                        flag = True
                        break
                start_hour = 0
            start_day = 1
        start_month = 1

        # podlist = []
        # for market in markets:
        #     z = name10.replace(markets[0], market)
        #     if os.path.exists(z):
        #         podlist.append(z)
        # listfiles.append(podlist)
    listfiles2 = []
    for file in listfiles:
        podlist = []
        podlist.append(file)
        for market in markets[1:]:
            z = file.replace(markets[0], market)
            if os.path.exists(z):
                podlist.append(z)
        # print(len(podlist),'==',len(markets))

        if onlymerge:
            if len(podlist)==len(markets):
                listfiles2.append(podlist)
        else:
            listfiles2.append(podlist)


    return listfiles2