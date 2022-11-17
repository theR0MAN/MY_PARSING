#
# a=[1,2,1,2,1,2]
# b=[1,2,3,4,5,6]
#
# a+=b
# print(a)
#
# a+='u'*len(b)
# print(a)
#
# c=[]
# v=[1]
# if c == v:
#     print('yes')
#
# a = {'e': [1, 2, 3, 4], 'b': [5, 6, 7, 8], 'c': [17, 18, 19, 20]}
# b = {'e': [9, 10, 11, 12], 'b': [13, 14, 15, 16], 'd': [21, 22, 23, 24]}
#
# fist_key = next(iter(b))
# ln = len(b[fist_key])
# for key in a:
#     if key in b:
#         a[key] += b[key]
#     else:
#         a[key] += [10] * ln
#
# print(a)
# #
# #
#
# z={}
# a = {'e': [1, 2, 'r', 4], 'b': [5, 6, 'r', 'r'], 'c': [17, 18, 'r', 20]}
# b = {'e': [9, 'r', 11, 12], 'b': [13, 14, 'r', 16], 'd': [21, 22, 23, 24]}
#
#
# fist_key = next(iter(b))
# ln = len(b[fist_key])
# for key in a:
#     if key in b:
#         a[key] += b[key]
#     else:
#         a[key] += 'r' * ln
# print(a)
#
#
# for key in a:
#     nom = -1
#     for el in a[key]:
#         nom+=1
#         # print(key,"  ",el,"  ",a[key][nom])
#         if el =='r':
#             a[key][nom]=a[key][nom-1]
#
# print(a)
# #
# a = {'e': [[1], {2:15}, [3], [4]], 'b': [[5], [6], [7], [8]], 'c': [[17], [18], [19], [20]]}
# b = {'e': [[9], [10], [11], [12]], 'b': [[13], [14], [15], [16]], 'd': [[21], [22], [23], [24]]}
#
# fist_key = next(iter(b))
# ln = len(b[fist_key])
# for key in a:
#     if key in b:
#         a[key] += b[key]
#     else:
#         a[key] += 'r' * ln
#
# print(a)
#
a = {'e': [{'a':10,'b':9},{'a':12,'b':11},{'a':114,'b':10}],'d': [{'a':100,'b':90},{'a':120,'b':110},{'a':1140,'b':100}] }

asks={}
bids={}

for key in a:
    for dcts in a[key]:
        # print(key,'  ',dcts,"   ",dcts['a'])
        if key not in asks:
            asks[key] =[]
            bids[key] = []
        asks[key].append(dcts['a'])
        bids[key].append(dcts['b'])
        # bids[key].append(dcts['b'])

print(a)
print(asks)
print(bids)