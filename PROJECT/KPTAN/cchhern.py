from PROJECT.my_lib import *

from collections import OrderedDict
dict_1 = {1: 'A', 2: 'B', 3: 'C'}
print("dict_1: ", dict_1)
dict_2 = dict(reversed(dict_1.items()))
print("dict_2: ", dict_2)