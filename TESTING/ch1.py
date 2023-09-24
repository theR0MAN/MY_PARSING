from GENERAL.G_FUNC import *
from platform import system
import plotly.express as px
import lzma as lz
import json
import time

# Нужно сделать многопоточку по одному инструменту, чтобы легче было проверить, результаты спаять.

markets=['FRTS']
onlymerge=0
in_instruments = [ 'NG-1.23*FRTS',  'NG-2.23*FRTS',  'NG-3.23*FRTS']
not_in_instruments = ['HANG']
start_year, start_month, start_day, start_hour = 2023, 1, 4, 14
stop_year, stop_month, stop_day, stop_hour = 	 2023, 1, 5, 15
fixkf=True
getpath = 'G:\\DATA_SBOR' if system() == 'Windows' else '/media/roman/J/DATA_SBOR'


content = getdata_merge(onlymerge,0,markets,getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour)
print(content)

 # Переделать все в разреженные массивы пандас упаковать используя Метод to_pickle()

# прописать  условия входа и выхода из сделок, создать словари где прописывается тип сделки (бай опен, бай клоуз,селопен,
# селлклоуз) цена сделки, объем аск или бид , время   ,  снапшот стакана во время сделки)
# для каждого файла  использовать мап синх, спаять результаты в конце  в словарь, вкатать словарь в файл для дальнейшей
# визуализации
# Переиграем. Каждая покупка и продажа записывается, а в постобработке уже определяется, что опен что клоуз
# так же пишется средний медианный объем по стакану  и средний спред.
# Односторонние сделки пишутся не чаще чем через  Н минут при условии что цена входа не совпадает с предыдущей

# сигнальная функция - получает входные параметры + стакан, возвращает только бай, селл, байклоуз, селлклоуз
# а лучше, получает котировки!
# Сперва простой патерн.

# Вход на смещении...
# Настройки - либо имеющийся объем    ( макс ограничен медиан*коэф)
# либо медианный с коэфом
# либо определенный по сумме.
# - считать средний спред,
# не принимать в расчет средней котиры со спредом в 10 или Н раз больше среднего -считать предыд    под вопросом...это
# -считать среднюю и в основе - отклонение инстр от средней
# Стреляем несколькими медианными объемами в сторону расхождения - вход на инстр со сбольшим смещением
# Работать только по заявкам которые можно забрать целиком
# Добавить возможность эмулирования неполного набора/закрытия  позиции с последующим добором/закрытием - для проверки
# эффективности работы по объемам - -приблизительно. Не закрывать по цене прошлого неполного закрытия.
# Проверить условие закрытия "только когда можно закрыть весь объём".
# Разнесённый по времени вход в сделку . Т.е взодим частями при сигнале не менее чем т времени
# старая классика - вход только с первого раза на объем, который получился.
#  уберем селлклоуз и байклоуз - сделаем симметрию для простоты
# ввести в отчет процент недобора позиции при закрытии
#  все же для учета контанго применить экстраполляцию спреда
# Тестирование самообучающейся модели.