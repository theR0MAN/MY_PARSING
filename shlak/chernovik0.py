#
# b = [1,2,3]
# c = [4,5,6]
# d = [7,8,9]
#
#
# for i in b:
#     print(i)
#     for i in c:
#         print(i)
#         for i in d:
#             print(i)

for i in range(3):
    print('1  ',i)
    for i in range(3):
        print('2  ',i)
        for i in range(3):
            print('3  ',i)