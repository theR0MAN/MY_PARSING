def numbers_range(n):
    for i in range(n):
        yield i
a = numbers_range(4)
print(type(a))
for b in a:
    print(b)
# Выведено в консоль будет:
# <class 'generator'>
# 0
# 1
# 2
# 3

# def numbers_range(n):
#     for i in range(n):
#         yield i
# a = numbers_range(4)
# print(next(a))
# print(next(a))
# print(next(a))
# print(next(a))
# Будет выведено в консоль
# 0
# 1
# 2
# 3