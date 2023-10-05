def getfut(l):
	'''
	принимает ключи (инструменты) в виде списка ['AED-12.23*FRTS', 'AED-3.24*FRTS', 'AED-6.24*FRTS',
	возвращает словарь фьючей   REZ [инструмент][]
	REZ [инструмент][0]-все фьючи
	REZ [инструмент][1]-с более поздним сроком экспирации
	REZ [инструмент][2] -с более ранним сроком экспирации
	:param l:
	:return:
	'''
	REZ=dict()
	for inst in l:
		if"-" in inst and '.' in inst:
			REZ[inst]=[]
			REZ[inst].append([])
			REZ[inst].append([])
			REZ[inst].append([])
	for inst0 in l:
		if"-" in inst0 and '.' in inst0:
			bodyit = inst0[:inst0.find('-')]
			x = inst0[inst0.find('-') + 1:inst0.find('*')].split(".")
			x2 = float(x[0]) + float(x[1]) * 12
			for inst in l:
				if "-" in inst and '.' in inst:
					bodyinst = inst[:inst.find('-')]
					xi = inst[inst.find('-') + 1:inst.find('*')].split(".")
					x2i = float(xi[0]) + float(xi[1]) * 12
					if bodyinst==bodyit and not x2==x2i:
						REZ[inst0][0].append(inst)
						if x2<x2i:
							REZ[inst0][1].append(inst)
						if x2>x2i:
							REZ[inst0][2].append(inst)
	return REZ