from FUNC import *
#
# def get_color():
#     i = 0
#     def func():
#         colors = ['black', 'red', 'blue', 'brown', 'green', 'violet', 'yellow', 'maroon', 'gold', 'pink', 'silver',
#                    'coral', 'chocolate']
#         colors0 = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure',
#                    'beige', 'bisque', 'black', 'blanchedalmond', 'blue',
#                    'blueviolet', 'brown', 'burlywood', 'cadetblue',
#                    'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
#                    'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan',
#                    'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen',
#                    'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange',
#                    'darkorchid', 'darkred', 'darksalmon', 'darkseagreen',
#                    'darkslateblue', 'darkslategray', 'darkslategrey',
#                    'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue',
#                    'dimgray', 'dimgrey', 'dodgerblue', 'firebrick',
#                    'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro',
#                    'ghostwhite', 'gold', 'goldenrod', 'gray', 'grey', 'green',
#                    'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo',
#                    'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen',
#                    'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan',
#                    'lightgoldenrodyellow', 'lightgray', 'lightgrey',
#                    'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen',
#                    'lightskyblue', 'lightslategray', 'lightslategrey',
#                    'lightsteelblue', 'lightyellow', 'lime', 'limegreen',
#                    'linen', 'magenta', 'maroon', 'mediumaquamarine',
#                    'mediumblue', 'mediumorchid', 'mediumpurple',
#                    'mediumseagreen', 'mediumslateblue', 'mediumspringgreen',
#                    'mediumturquoise', 'mediumvioletred', 'midnightblue',
#                    'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy',
#                    'oldlace', 'olive', 'olivedrab', 'orange', 'orangered',
#                    'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise',
#                    'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink',
#                    'plum', 'powderblue', 'purple', 'red', 'rosybrown',
#                    'royalblue', 'rebeccapurple', 'saddlebrown', 'salmon',
#                    'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver',
#                    'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow',
#                    'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato',
#                    'turquoise', 'violet', 'wheat', 'white', 'whitesmoke',
#                    'yellow', 'yellowgreen']
#         nonlocal i
#         i += 1
#         if i<13:
#             return colors[i]
#         else:
#             return random.choice(colors0)
#
#     return func

color = get_color()
clr=color()

print(clr)
print(type(clr))
#
# print(color())
# print(color())
# print(color())
# print(color())
# print(color())
# print(color())
# print(color())
# print(color())
# print(color())
# print(color())
# print(color())
# print(color())
# print(color())
# print(color())
# print(color())

# z=random.choice(colors)
# z2=random.choice(colors2)
#
# print(z)
# print(z2)
#
# def create_counter():
#     # global i
#     i = 0
#
#     def func():
#         nonlocal i
#         i += 1
#         return i
#
#     return func
#
# counter = create_counter()
# print(counter())  # 1
# print(counter())  # 2
# print(counter())  # 3
#
#
# def create_counter2(i):
#     def func():
#         nonlocal i
#         i += 1
#         return i
#     return func
#
# counter2 = create_counter2(5)
# print(counter2())  # 1
# print(counter())  # 2
# print(counter())  # 3