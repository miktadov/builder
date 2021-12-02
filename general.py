from boards import *
from image import make_image, estimate


class Wall:
	def __init__(self, width, height, space=625, lc=False, rc=False, b=[50,150, 6000], doors=[], windows=[]):
		errors(width, height, b, doors, windows, [lc, rc])
		
		self.osb = []
		self.osb_cuts = []
		self.wata50 = 0
		self.wata100 = 0
		self.width = width
		self.hight = height
		self.board = b
		self.bs = bs = []
		self.space = space
		self.lvl = [0, False]
		self.lc = lc
		self.rc = rc
		self.doors = doors
		self.windows = windows

		self.woods = []
		self.nails = 0
		self.vapor_barrier = 0.0
		self.wind_protection = 0.0
		self.rail = []
		
		# ВЕРХНЯЯ И НИЖНЯЯ ОБВЯЗКА
		# 1 нижняя обвязка
		if doors:
			x = 0
			for door in doors:
				if door.x1[0]-x > b[2]:
					while x+b[2] < door.x1[0]:
						wood = Board([x, 0], [x+b[2], b[0]], p=b)
						bs.append(wood)
						x += b[2]
				wood = Board([x, 0], ori='h', length=door.x1[0]-x, p=b)
				bs.append(wood)
				x = door.x2[0]
				
				
			wood = Board([x, 0], [width, b[0]], p=b)
			bs.append(wood)
		else:
			x=0
			if width > b[2]:
				while x+b[2] < width:
					wood = Board([x, 0], [x+b[2], b[0]], p=b)
					bs.append(wood)
					x += b[2]
			wood = Board([x, 0], [width, b[0]], p=b)
			bs.append(wood)
		# 3 верхняя обвязка
		x = 0
		if width > b[2]:
			while x+b[2] < width:
				wood = Board([x, height-b[0]], ori='h', length=b[2], p=b)
				bs.append(wood)
				x += b[2]
		wood = Board([x, height-b[0]], [width, height], p=b)
		ln = width - x
		bs.append(wood)
		# 2 верхняя обвязка
		x = 0
		if ln > b[2] - 1000:
			ln -= int(b[2] / 2)
		elif ln < 1000:
			ln += int(b[2] / 2)
		if width > b[2]:
			while x+b[2] < width:
				wood = Board([x, height-b[0]*2], ori='h', length=ln, p=b, ser='ng')
				bs.append(wood)
				x += ln
				ln = b[2]
		wood = Board([x, height-b[0]*2], [width, height-b[0]], p=b, ser='ng')
		bs.append(wood)
		# КОНЕЦ ВЕРХНЕЙ И НИЖНЕЙ ОБВЯЗКИ
		
		
		# ВЕРТИКАЛЬНЫЕ СТОЙКИ
		x = 0
		wood = Board([x, b[0]], length=height-b[0]*3, p=b)
		bs.append(wood) # Первая стойка
		if not lc:
			wood = Board([b[0], b[0]], [b[0]+b[1], height-b[0]*2], p=b)
			bs.append(wood) # Левая соединительная стойка
		if not rc:
			wood = Board([width-b[1]-b[0], b[0]], [width-b[0], height-b[0]*2], p=b)
			bs.append(wood) # Правая соединительная стойка
			
		x += int(space - b[0] / 2) - lc
		stoyka = 0
		while  x <= width - b[0] * 2:
			
			key = True
			if windows:				
				for w in windows:
					if x+b[0] > w.left_left and x < w.right_right:
						key, dwn_have = False, True
						if x > w.left and x+b[0] < w.right: # Центр
							if x < w.left + b[0] + b[0] * w.wpb:
								if x < w.left + b[0] * w.wpb:
									dwn_have = False
								else:
									pos = w.left + b[0] + b[0] * w.wpb
							elif x + b[0] > w.right - b[0] - b[0] * w.wpb:
								if x > w.right - b[0] - b[0] * w.wpb:
									dwn_have = False
								else:
									pos = w.right - b[0] * 2 - b[0] * w.wpb
							else:
								pos = x
							if dwn_have:
								bs.append(Board([pos, b[0]], [pos+b[0], w.x1[1]-b[0]], p=b))
							wood = Board([x, w.win_hight], [x+b[0], height-b[0]*2], p=b)
						elif x < w.left_left and x+b[0] > w.left_left: # Слева от лева
							wood = Board([w.left_left-b[0], b[0]], length=height-b[0]*3, p=b)
						elif x < w.left and x+b[0] > w.left: # Справа от лева
							wood = Board([w.left, w.win_hight], [w.left+b[0], height-b[0]*2], p=b)
						elif x < w.right and x+b[0] > w.right: # Слева от права
							wood = Board([w.right-b[0], w.win_hight], [w.right, height-b[0]*2], p=b)
						elif x < w.right_right and x+b[0] > w.right_right: # Справа от права
							wood = Board([w.right_right, b[0]], length=height-b[0]*3, p=b)
						else: # Доска попала четко на стойку
							x += space
							stoyka += 1
							break
						bs.append(wood)
						x += space
						break
			
			if doors and key:
				for d in doors:
					if x+b[0] > d.left_left and x < d.right_right:
						key = False
						if x > d.left and x+b[0] < d.right: # Центр
							wood = Board([x, d.door_hight], [x+b[0], height-b[0]*2], p=b)
						elif x < d.left_left and x+b[0] > d.left_left: # Слева от лева
							wood = Board([d.left_left-b[0], b[0]], length=height-b[0]*3, p=b)
						elif x < d.left and x+b[0] > d.left: # Справа от лева
							wood = Board([d.left, d.door_hight], [d.left+b[0], height-b[0]*2], p=b)
						elif x < d.right and x+b[0] > d.right: # Слева от права
							wood = Board([d.right-b[0], d.door_hight], [d.right, height-b[0]*2], p=b)
						elif x < d.right_right and x+b[0] > d.right_right: # Справа от права
							wood = Board([d.right_right, b[0]], length=height-b[0]*3, p=b)
						else: # Доска попала четко на стойку
							x += space
							stoyka += 1
							break
						bs.append(wood)
						x += space
						break
						
			if key:
				if x >= b[0] and x < b[0]+b[1]: # Попала на левую соед. стойку
					b2 = [b[0], b[1]-b[0], b[2]]
				elif x+b[0] > width-b[1]-b[0] and x+b[0] <= width-b[0]: # Попала на правую соед. стойку
					b2 = [b[0], b[1]-b[0], b[2]]
				else:
					b2 = b
				wood = Board([x, b[0]], length=height-b[0]*3, p=b2)
				bs.append(wood)
				x += space
			
		if x > width - b[0] * 2 and x < width - b[0]: # Если доска нахлестом
			wood = Board([width-b[0]*2, b[0]], length=height-b[0]*3, p=b)
			bs.append(wood)
		
		wood = Board([width - b[0], b[0]], length=height-b[0]*3, p=b)
		bs.append(wood) # Последняя стойка
		# КОНЕЦ ВЕРТИКАЛЬНЫХ СТОЕК
			
			# СОЗДАНИЕ ОКОННЫХ ПРОЕМОВ
		c, s = 1, ''
		for w in windows:
			bs.append(Board([w.left_left, b[0]], length=height-b[0]*3, p=b))
			bs.append(Board([w.right_right-b[0], b[0]], length=height-b[0]*3, p=b))
			bs.append(Board([w.left, w.x2[1]], [w.right, w.x2[1]+b[0]], p=b))
			bs.append(Board([w.left, w.x2[1]+b[0]], [w.right, w.win_hight], p=b, ser='ng'))
			bs.append(Board([w.left, w.x2[1]+b[0]], [w.right, w.win_hight], p=b, ser='ng'))
			bs.append(Board([w.left, w.x1[1]-b[0]], [w.right, w.x1[1]], p=b))
			l, r = w.left, w.right-b[0]
			for count in range(1+w.wpb):
				if c > 1:
					s = 'ng'
				bs.append(Board([l, w.x1[1]], [l+b[0], w.x2[1]], p=b, ser=s))
				bs.append(Board([r, w.x1[1]], [r+b[0], w.x2[1]], p=b, ser=s))
				bs.append(Board([l, b[0]], [l+b[0], w.x1[1]-b[0]], p=b, ser=s))
				bs.append(Board([r, b[0]], [r+b[0], w.x1[1]-b[0]], p=b, ser=s))
				l += b[0]
				r -= b[0]
		
			# СОЗДАНИЕ ДВЕРНЫХ ПРОЕМОВ
		c, s = 1, ''
		for d in doors:
			bs.append(Board([d.left_left, b[0]], length=height-b[0]*3, p=b))
			bs.append(Board([d.right_right-b[0], b[0]], length=height-b[0]*3, p=b))
			bs.append(Board([d.left, d.x2[1]], [d.right, d.x2[1]+b[0]], p=b))
			bs.append(Board([d.left, d.x2[1]+b[0]], [d.right, d.door_hight], p=b, ser='ng'))
			bs.append(Board([d.left, d.x2[1]+b[0]], [d.right, d.door_hight], p=b, ser='ng'))
			l, r = d.left, d.right-b[0]
			for count in range(1+d.wpb):
				if c > 1:
					s = 'ng'
				bs.append(Board([l, b[0]], [l+b[0], d.x2[1]], p=b, ser=s))
				bs.append(Board([r, b[0]], [r+b[0], d.x2[1]], p=b, ser=s))
				l += b[0]
				r -= b[0]

	def wata(self, pogr):
		if pogr != 0:
			pogr = pogr / 100 + 1
		else:
			pogr = 1
		p_wall = self.width/1000 * self.hight/1000
		p_cut, p_cut2 = [], []
		if self.windows:
			for w in self.windows:
				p_cut.append(w.width/1000 * w.hight/1000)
		if self.doors:
			for d in self.doors:
				p_cut.append(d.width/1000 * d.hight/1000)
		for b in self.bs:
			if b.width == self.board[0] or b.hight == self.board[0]:
				p_cut.append(b.width/1000 * b.hight/1000)
			else:
				p_cut2.append(b.width/1000 * b.hight/1000)
		p = p_wall - sum(p_cut)
		p_cut2 = sum(p_cut2)
		if int(self.board[1]/50) == 1:
			self.wata50 = round((p-p_cut2/2)*pogr, 2)
		elif int(self.board[1]/50) == 2:
			self.wata50 = round(p_cut2/2*pogr, 2)
			self.wata100 = round(p*pogr, 2)
		elif int(self.board[1]/50) == 3:
			self.wata50 = round((p-p_cut2)*pogr, 2)
			self.wata100 = round(p*pogr, 2)
		elif int(self.board[1]/50) == 4:
			self.wata100 = round((p-p_cut2/2)*2*pogr, 2)

	def make_osb(self, s=[2500, 1250], lvl=[0, False], lc=False, rc=False):
		if lvl[1]:
			hight = self.hight + lvl[1]
		else:
			hight = self.hight
		self.lvl = lvl
		x = [0-lc, 0-lvl[0]]
		wi = self.width + rc
		hi = self.hight
		sw = s[0]
		sh = s[1]
		lay = 1
		while x[1] <= hight:
			if lay%2 == 0:
				x[0] = int(0 - lc - s[0] / 2)
			else:
				x[0] = 0 - lc
			lay += 1
			if x[1]+sh < hi:
				h = x[1] + sh
			else:
				h = hight
			
			while x[0] < wi:
				if x[0]+sw < wi:
					w = x[0] + s[0]
				else:
					w = wi
					
				osb = OSB([x[0], x[1]], width=s[0], hight=s[1])
				self.osb.append(osb)
				x[0] += sw
			x[1] += sh
	
		for o in self.osb:
			if o.x1[0] < 0-lc:
				osb = OSB(o.x1, [0-lc, o.x2[1]], is_cut=True, ser=o.serial)
				self.osb_cuts.append(osb)
				o.x1[0] = 0-lc
				o.save()
			if o.x2[0] > wi:
				osb = OSB([wi, o.x1[1]], o.x2, is_cut=True, ser=o.serial)
				self.osb_cuts.append(osb)
				o.x2[0] = wi
				o.save()
			if o.x2[1] > hi:
				osb = OSB([o.x1[0], hi], o.x2, is_cut=True, ser=o.serial)
				self.osb_cuts.append(osb)
				o.x2[1] = hi
				o.save()
		
		return self.osb_cuts


width_wall = 10000
height_wall = 3150
board_pitch_wall = 625
lc = 0								# left overlap			левый нахлест
rc = 0								# right overlap			правый нахлест
lvl = [0, 0]						# [up, down] overlap	[верхний, нижний] нахлест
image_indent = [
	100+lc,
	100+lvl[1],
	100+rc,
	100+lvl[0]
]				# image indent			отступ изображения
board = [50, 150, 6000]				# Board dimensions		размеры доски
vapor_barier = [1.6, 10]
wind_protection = [1.6, 20]

doors = [
	Door(							# первая дверь
		[5000, 0], 						# координаты левой нижней точки
		[5980, 2071], 					# координаты правой верхней точки
		b=board							# размер доски
	),
	Door(							# вторая дверь
		[7000, 0], 						# координаты левой нижней точки
		width=2000, 					# ширина
		hight=1071, 					# высота
		b=board							# размер доски
	)
]
windows = [
	Window(							# первое окно
		[1000, 1000], 					# координаты левой нижней точки
		width=1000, 					# ширина
		hight=1000, 					# высота
		b=board							# размер доски
	),
	Window(							# второе окно
		[3000, 400],  					# координаты левой нижней точки
		width=500,  					# ширина
		hight=2000,  					# высота
		b=board							# размер доски
	)
]


wall = Wall(
	width=width_wall,
	height=height_wall,
	space=board_pitch_wall,
	lc=lc,
	rc=rc,
	b=board,
	doors=doors,
	windows=windows)

wall.woods = compress_boards(wall.bs, board)						# подсчет полноразмерных досок
wall.wata(5)														# подсчет утеплителя
wall.make_osb(lvl=lvl, lc=lc, rc=rc)								# подсчет ОСБ плит
wall.vapor_barrier = make_vapor_barrier(wall, vapor_barier)			# подсчет пароизоляции
wall.wind_protection = make_wind_protection(wall, wind_protection)	# подсчет ветро-гидрозащиты
wall.nails = nails_osb(wall.bs)										# подсчет гвоздей
wall.rail = rail(wall)												# подсчет брусков
# for i in wall.bs:
# 	print(f'{i.x1[0]}:{i.x1[1]}     \t{i.x2[0]}:{i.x2[1]} \t{i.par[0]}x{i.par[1]}x{i.length}\t{i.serial}')
# print('\n\t', len(wall.bs), ' Обрезка доски\n')

# for i in wall.osb:
# 	print(f'{i.x1[0]}:{i.x1[1]}   \t{i.x2[0]}:{i.x2[1]} \t{i.width}x{i.hight}  \t{i.serial}')
# print('\n\t', len(wall.osb), ' ОСБ плиты\n')

# for i in osb_cuts:
# 	print(f'{i.x1[0]}:{i.x1[1]}   \t{i.x2[0]}:{i.x2[1]} \t{i.width}x{i.hight}   \t{i.serial}')
# 	print(i.x1, ' ', i.x2)
# print('\n\t', len(wall.osb_cuts), ' Обрезков от ОСБ\n')
estimate(wall)														# создание сметы
make_image(															# создание изображения
	wall,
	image_indent)
			