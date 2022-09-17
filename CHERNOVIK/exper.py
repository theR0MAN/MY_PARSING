
# file_name = '/media/roman/J/Открытие ФОРТС/MQL5/Files/PERkuklfondahistoryall/452733.txt'
# file = open(file_name, mode='r',encoding='utf-16')  # mode (режим): чтение бинарное
# file_content = file.read()
# z= len(file_content)
# file.close()
#
# file_name = '/media/roman/J/Открытие ФОРТС/MQL5/Files/PERkuklfondahistoryall/452734.txt'
# file = open(file_name, mode='r',encoding='utf-16')  # mode (режим): чтение бинарное
# file_content += file.read()
# x= len(file_content)
# file.close()
#
# file_name = '/media/roman/J/Открытие ФОРТС/MQL5/Files/PERkuklfondahistoryall/452747.txt'
# file = open(file_name, mode='r',encoding='utf-16')  # mode (режим): чтение бинарное
# file_content += file.read()
# u= len(file_content)
# file.close()
#
#
# print(file_content)
# print(z,"       ",x,"       ",u)
#


text_file = open('/media/roman/J/Открытие ФОРТС/MQL5/Files/PERkuklfondahistoryall/452733.txt', mode='r',encoding='utf-16')
lines = text_file.read().split()
print (lines)
text_file.close()


# https://psyclinic-center.ru/biblioteka-kliniki/vvedenie-v-klinicheskuyu-psihiatriyu
# http://psyclinic-center.ru/biblioteka-kliniki/vvedenie-v-klinicheskuyu/razmytie-granic-vremeni-oshchushchenie-uzhe-perezhitogo
# https://mayaksbor.ru/news/society/opukholi_epilepsiya_i_shizofreniya_chem_effekt_dezhavyu_opasen_dlya_zdorovya/




