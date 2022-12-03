import subprocess





a = {'3551': {'a': 13644.0, 'b': 13642.0,
			  'asks': [[13644.0, 1], [13645.0, 39], [13646.0, 21], [13647.0, 59], [13648.0, 34], [13649.0, 8],
					   [13650.0, 58], [13651.0, 42], [13652.0, 41], [13653.0, 35], [13654.0, 15], [13655.0, 16],
					   [13656.0, 17], [13657.0, 10], [13658.0, 31], [13659.0, 75], [13660.0, 75], [13661.0, 18],
					   [13662.0, 22], [13663.0, 46]],
			  'bids': [[13642.0, 6], [13641.0, 8], [13640.0, 14], [13639.0, 14], [13638.0, 26], [13637.0, 37],
					   [13636.0, 10], [13635.0, 54], [13634.0, 79], [13632.0, 21], [13631.0, 32],
					   [13630.0, 29], [13629.0, 64], [13628.0, 68], [13627.0, 141], [13626.0, 26], [13625.0, 74],
					   [13624.0, 78], [13623.0, 69]]}, '3552': {'a': 13645.0, 'b': 13642.0,
																'asks': [[13645.0, 39], [13646.0, 21], [13647.0, 59],
																		 [13648.0, 34], [13649.0, 8], [13650.0, 58],
																		 [13651.0, 42], [13652.0, 41], [13653.0, 35],
																		 [13654.0, 15], [13655.0, 16], [13656.0, 17],
																		 [13657.0, 10], [13658.0, 31], [13659.0, 75],
																		 [13660.0, 75], [13661.0, 18], [13662.0, 22],
																		 [13663.0, 46], [13664.0, 17]],
																'bids': [[13642.0, 6], [13641.0, 8], [13640.0, 14],
																		 [13639.0, 14], [13638.0, 26], [13637.0, 37],
																		 [13636.0, 10], [13635.0, 54], [13634.0, 79],
																		 [13633.0, 162], [13632.0, 21], [13631.0, 32],
																		 [13630.0, 29], [13629.0, 64], [13628.0, 68],
																		 [13627.0, 141], [13626.0, 26], [13625.0, 74],
																		 [13624.0, 78], [13623.0, 69]]},
	 '3553': {'a': 13642.0, 'b': 13640.0,
			  'asks': [[13642.0, 1], [13643.0, 3], [13644.0, 5], [13645.0, 39], [13646.0, 15], [13647.0, 59],
					   [13648.0, 34], [13649.0, 8], [13650.0, 58], [13651.0, 42], [13652.0, 43], [13653.0, 37],
					   [13654.0, 15], [13655.0, 16], [13656.0, 17], [13657.0, 12], [13658.0, 31], [13659.0, 75],
					   [13660.0, 75], [13661.0, 18]],
			  'bids': [[13640.0, 40], [13639.0, 9], [13638.0, 29], [13637.0, 37], [13636.0, 23], [13635.0, 59],
					   [13634.0, 64], [13633.0, 162], [13632.0, 21], [13631.0, 31], [13630.0, 29], [13629.0, 66],
					   [13628.0, 68], [13627.0, 162], [13626.0, 29], [13625.0, 63], [13624.0, 89], [13623.0, 69],
					   [13622.0, 120], [13621.0, 104]]}}
def viz_stakan(a):
	def frmt(value, len_zapis, prefix, zapoln):
		v1 = (prefix + str(value))[:len_zapis]
		if len(v1) < len_zapis:
			v1 += (len_zapis - len(v1)) * zapoln
		return v1
	# максимум и минимум цены
	masmax = []
	masmin = []
	for key in a:
		masmax.append(a[key]['asks'][len(a[key]['asks']) - 1][0])
		masmin.append(a[key]['bids'][len(a[key]['bids']) - 1][0])
	mx = max(masmax)
	mn = min(masmin)
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
	shag = int(min(masrazn))
	maxlen += 1
	# первый аск
	firstask = a[next(iter(a))]['asks'][0][0]
	# первый bid
	firstbid = a[next(iter(a))]['bids'][0][0]
	firstmed = (firstbid + firstask) / 2
	# количество шагов
	kvo_str = int((mx - mn) / shag)
	# строка по первому аску , заодно  формула номера строки для цен
	first = int((mx - firstask) / shag)
	# вывод шкалы процентных изменений цены от первой цены аск,  - первый столбец
	koef = 100 / firstmed
	mmax = mx * koef
	mshag = shag * koef
	skala = []
	for i in range(kvo_str):
		skala.append(round(mmax - mshag * i, 2))
	# нормализация словаря замена  таймстампа на столбцы, цен -на строки, объемы аски с "+" биды с"-"
	# первц столбец -на шкалу
	b = {}
	nom_stlb = 0
	for key in a:
		nom_stlb += 1
		b[str(nom_stlb)] = dict()
		b[str(nom_stlb)]['asks'] = {}
		b[str(nom_stlb)]['bids'] = {}
		b[str(nom_stlb)]['all'] = {}
		for n in a[key]['asks']:
			b[str(nom_stlb)]['asks'][str(int((mx - n[0]) / shag))] = frmt(n[1], maxlen, "+", ' ')
		for n in a[key]['bids']:
			b[str(nom_stlb)]['bids'][str(int((mx - n[0]) / shag))] = frmt(n[1], maxlen, "-", ' ')
		# соединяем аски и биды  в один словарь
		b[str(nom_stlb)]['all'] = b[str(nom_stlb)]['asks'] | b[str(nom_stlb)]['bids']
	kvo_stlb = len(b) + 1

	# переводим словарь в массив
	mas = [maxlen * " "] * kvo_str
	for i in range(kvo_str):
		mas[i] = [maxlen * " "] * kvo_stlb
	for i in range(kvo_str):
		mas[i][0] = frmt(skala[i], 10, "", ' ')
	for i in range(kvo_str):
		for j in range(1, kvo_stlb):
			if str(j) in b and str(i) in b[str(j)]['all']:
				mas[i][j] = b[str(j)]['all'][str(i)]
	with open('STAKAN.txt', mode='w') as f:
		for i in range(kvo_str):
			f.write(''.join(mas[i]) + '\n')

	subprocess.run(["C:\\Users\\milro\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe", "STAKAN.txt"])

viz_stakan(a)