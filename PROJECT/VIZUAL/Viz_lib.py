import random
import os
import pandas as pd

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
		if i < 13:
			return colors[i]
		else:
			return random.choice(colors0)

	return func




def viz_stakan2(a, a2):
	def frmt(value, len_zapis, prefix, zapoln):
		v1 = (str(value) + prefix)[:len_zapis]
		if len(v1) < len_zapis:
			v1 += (len_zapis - len(v1)) * zapoln
		return v1

	if len(a) == 0:
		print('len<0  quit')
		quit()

	# шаг цены и ширина ячейки объема
	masrazn = []
	maxlen = 0
	for key in a:
		bidcens = []
		askcens = []
		for i in a[key]['asks']:
			askcens.append(i[0])
			maxlen = max(maxlen, len(str(i[1])))
		for i in a[key]['bids']:
			bidcens.append(i[0])
			maxlen = max(maxlen, len(str(i[1])))
		askcens.reverse()
		z = askcens + bidcens
		for i in range(1, len(z)):
			razn = z[i - 1] - z[i]
			masrazn.append(razn)
	shag = min(masrazn)

	# первый midl  a
	firstask = a[next(iter(a))]['asks'][0][0]
	firstbid = a[next(iter(a))]['bids'][0][0]
	firstmeda = (firstbid + firstask) / 2

	# первый midl  b
	firstask = a2[next(iter(a2))]['asks'][0][0]
	firstbid = a2[next(iter(a2))]['bids'][0][0]
	firstmeda2 = (firstbid + firstask) / 2

	koefa2a = firstmeda / firstmeda2
	# Нормализация цен второго массива к мервому с привязкой по первой медиане
	a3 = {}
	for key in a2:
		for cenlist in a2[key]['asks']:
			maxlen = max(maxlen, len(str(cenlist[1])))
		for cenlist in a2[key]['bids']:
			maxlen = max(maxlen, len(str(cenlist[1])))

	maxlen += 2
	for key in a2:
		a3[key] = dict()
		a3[key]['asks'] = []
		a3[key]['bids'] = []
		for cenlist in a2[key]['asks']:
			a3[key]['asks'].append([round(cenlist[0] * koefa2a / shag) * shag, frmt(cenlist[1], maxlen, "ps", ' ')])
		# print(f'{koefa2a} cenlist  {cenlist}    a3[key]["asks"]   {a3[key]["asks"]}')
		for cenlist in a2[key]['bids']:
			a3[key]['bids'].append([round(cenlist[0] * koefa2a / shag) * shag, frmt(cenlist[1], maxlen, "ms", ' ')])

	# переформатну ка я первый словарь по объемам
	a0 = {}
	for key in a:
		a0[key] = dict()
		a0[key]['asks'] = []
		a0[key]['bids'] = []
		for cenlist in a[key]['asks']:
			a0[key]['asks'].append([cenlist[0], frmt(cenlist[1], maxlen, "pf", ' ')])
		# print(f'{koefa2a} cenlist  {cenlist}    a3[key]["asks"]   {a0[key]["asks"]}')
		for cenlist in a[key]['bids']:
			a0[key]['bids'].append([cenlist[0], frmt(cenlist[1], maxlen, "mf", ' ')])

	# имеем два словаря	a0  a3 , замержим их
	# переименую, бо некрасиво, брутфорс -сила
	c1 = a0
	c2 = a3
	lastc1 = c1[next(iter(c1))]
	lastc2 = c2[next(iter(c2))]

	d3 = {}
	numc = 1
	startkey = min(int(next(iter(c1))), int(next(iter(c2))))
	print(startkey)
	for ikey in range(startkey, 3600):
		yes = False
		if str(ikey) in c1:
			lastc1 = c1[str(ikey)]
			yes = True
		if str(ikey) in c2:
			lastc2 = c2[str(ikey)]
			yes = True

		if yes:
			d3[str(numc)] = lastc1
			d3[str(numc + 1)] = lastc2
			numc += 2

	# максимум и минимум цены
	masmax = []
	masmin = []
	for key in d3:
		masmax.append(d3[key]['asks'][len(d3[key]['asks']) - 1][0])
		masmin.append(d3[key]['bids'][len(d3[key]['bids']) - 1][0])

	mx = max(masmax)
	mn = min(masmin)

	# количество шагов
	kvo_str = int((mx - mn) / shag)
	# строка по первому аску , заодно  формула номера строки для цен
	first = int((mx - firstask) / shag)
	# вывод шкалы процентных изменений цены от первой цены аск,  - первый столбец
	koef = 100 / firstmeda
	mmax = mx * koef
	mshag = shag * koef
	skala = []
	for i in range(kvo_str):
		skala.append(round(mmax - mshag * i, 2))
	# нормализация словаря замена  таймстампа на столбцы, цен -на строки, объемы аски с "+" биды с"-"
	# первц столбец -на шкалу
	# maxstlb=12000/maxlen
	b = {}
	for key in d3:
		b[key] = dict()
		b[key]['asks'] = {}
		b[key]['bids'] = {}
		b[key]['all'] = {}
		for n in d3[key]['asks']:
			b[key]['asks'][str(int((mx - n[0]) / shag))] = n[1]
		for n in d3[key]['bids']:
			b[key]['bids'][str(int((mx - n[0]) / shag))] = n[1]
		# соединяем аски и биды  в один словарь
		b[key]['all'] = b[key]['asks'] | b[key]['bids']
	kvo_stlb = len(b) + 1

	# переводим словарь в массив
	mas = [(maxlen) * " "] * kvo_str
	for i in range(kvo_str):
		mas[i] = [(maxlen) * " "] * kvo_stlb
	for i in range(kvo_str):
		mas[i][0] = frmt(skala[i], 10, " ", ' ')
	for i in range(kvo_str):
		for j in range(1, kvo_stlb):
			if str(j) in b and str(i) in b[str(j)]['all']:
				mas[i][j] = b[str(j)]['all'][str(i)]
	with open('STAKAN.txt', mode='w') as f:
		for i in range(kvo_str):
			f.write(''.join(mas[i]) + '\n')

	df = pd.DataFrame(mas)
	df.to_excel('F:\\Все\\MY_PARSING\\GENERAL\\teams.xlsx', index=False, header=False)
	print(df)
	# subprocess.run(["C:\\Users\\milro\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe", "STAKAN.txt"])
	os.system('start excel.exe teams.xlsx')


def viz_stakan1(a):
	def frmt(value, len_zapis, prefix, zapoln):
		v1 = (str(value) + prefix)[:len_zapis]
		if len(v1) < len_zapis:
			v1 += (len_zapis - len(v1)) * zapoln
		return v1

	if len(a) == 0:
		print('len<0  quit')
		quit()

	# шаг цены и ширина ячейки объема
	masrazn = []
	maxlen = 0
	for key in a:
		bidcens = []
		askcens = []
		for i in a[key]['asks']:
			askcens.append(i[0])
			maxlen = max(maxlen, len(str(i[1])))
		for i in a[key]['bids']:
			bidcens.append(i[0])
			maxlen = max(maxlen, len(str(i[1])))
		askcens.reverse()
		z = askcens + bidcens
		for i in range(1, len(z)):
			razn = z[i - 1] - z[i]
			masrazn.append(razn)
	shag = min(masrazn)

	# первый midl  a
	firstask = a[next(iter(a))]['asks'][0][0]
	firstbid = a[next(iter(a))]['bids'][0][0]
	firstmeda = (firstbid + firstask) / 2

	maxlen += 2
	# переформатну ка я первый словарь по объемам
	a0 = {}
	for key in a:
		a0[key] = dict()
		a0[key]['asks'] = []
		a0[key]['bids'] = []
		for cenlist in a[key]['asks']:
			a0[key]['asks'].append([cenlist[0], frmt(cenlist[1], maxlen, "pf", ' ')])
		for cenlist in a[key]['bids']:
			a0[key]['bids'].append([cenlist[0], frmt(cenlist[1], maxlen, "mf", ' ')])

	# имеем два словаря	a0  a3 , замержим их
	# переименую, бо некрасиво, брутфорс -сила
	lastc1 = a0[next(iter(a0))]

	d3 = {}
	numc = 1
	startkey = int(next(iter(a0)))
	print(startkey)
	for ikey in range(startkey, 3600):
		if str(ikey) in a0:
			lastc1 = a0[str(ikey)]
			d3[str(numc)] = lastc1
			numc += 1

	# максимум и минимум цены
	masmax = []
	masmin = []
	for key in d3:
		masmax.append(d3[key]['asks'][len(d3[key]['asks']) - 1][0])
		masmin.append(d3[key]['bids'][len(d3[key]['bids']) - 1][0])

	mx = max(masmax)
	mn = min(masmin)

	# количество шагов
	kvo_str = int((mx - mn) / shag)
	# строка по первому аску , заодно  формула номера строки для цен
	first = int((mx - firstask) / shag)
	# вывод шкалы процентных изменений цены от первой цены аск,  - первый столбец
	koef = 100 / firstmeda
	mmax = mx * koef
	mshag = shag * koef
	skala = []
	for i in range(kvo_str):
		skala.append(round(mmax - mshag * i, 2))
	# нормализация словаря замена  таймстампа на столбцы, цен -на строки, объемы аски с "+" биды с"-"
	# первц столбец -на шкалу
	# maxstlb=12000/maxlen
	b = {}
	for key in d3:
		b[key] = dict()
		b[key]['asks'] = {}
		b[key]['bids'] = {}
		b[key]['all'] = {}
		for n in d3[key]['asks']:
			b[key]['asks'][str(int((mx - n[0]) / shag))] = n[1]
		for n in d3[key]['bids']:
			b[key]['bids'][str(int((mx - n[0]) / shag))] = n[1]
		# соединяем аски и биды  в один словарь
		b[key]['all'] = b[key]['asks'] | b[key]['bids']
	kvo_stlb = len(b) + 1

	# переводим словарь в массив
	mas = [(maxlen) * " "] * kvo_str
	for i in range(kvo_str):
		mas[i] = [(maxlen) * " "] * kvo_stlb
	for i in range(kvo_str):
		mas[i][0] = frmt(skala[i], 10, " ", ' ')
	for i in range(kvo_str):
		for j in range(1, kvo_stlb):
			if str(j) in b and str(i) in b[str(j)]['all']:
				mas[i][j] = b[str(j)]['all'][str(i)]
	with open('STAKAN.txt', mode='w') as f:
		for i in range(kvo_str):
			f.write(''.join(mas[i]) + '\n')

	df = pd.DataFrame(mas)
	df.to_excel('F:\\Все\\MY_PARSING\\GENERAL\\teams.xlsx', index=False, header=False)
	print(df)
	# subprocess.run(["C:\\Users\\milro\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe", "STAKAN.txt"])
	os.system('start excel.exe teams.xlsx')