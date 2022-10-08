import MetaTrader5 as mt5

# выведем данные о пакете MetaTrader5
print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)

# установим подключение к терминалу MetaTrader 5 на указанный торговый счет
if not mt5.initialize(login=91066, server="Open-Broker", password="Milroal6553024"):
	print("initialize() failed, error code =", mt5.last_error())
	quit()

#
#
# # выведем данные о торговом счете как есть
# print(mt5.account_info())
# # выведем данные о торговом счете в виде списка
# print("Show account_info()._asdict():")
# account_info_dict = mt5.account_info()._asdict()
# for prop in account_info_dict:
# 	print("  {}={}".format(prop, account_info_dict[prop]))
#
# # получим количество финансовых инструментов
# symbols=mt5.symbols_total()
# if symbols>0:
#     print("Total symbols =",symbols)
# else:
#     print("Symbols not found")

# выведем свойства по символу EURJPY
symbol_info=mt5.symbol_info("GAZR-12.22")
if symbol_info!=None:
    # выведем данные о терминале как есть
    print(symbol_info)
    print("GAZR-12.22: spread =",symbol_info.spread,"  digits =",symbol_info.digits)
    # # выведем свойства символа в виде списка
    # print("Show symbol_info(\"GAZR-12.22\")._asdict():")
    # symbol_info_dict = mt5.symbol_info("GAZR-12.22")._asdict()
    # for prop in symbol_info_dict:
    #     print("  {}={}".format(prop, symbol_info_dict[prop]))
	#


# завершим подключение к терминалу MetaTrader 5
mt5.shutdown()