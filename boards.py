sb = 1
so = 1

class Board:
	def __init__(self, x1, x2=False, ori='v', length=6000, ser='', p=[50, 150, 6000]):
		self.x1 = x1
		if x2:
			self.x2 = x2
		else:
			if ori == 'h':
				self.x2 = x2 = [x1[0]+length, x1[1]+p[0]]
			else:
				self.x2 = x2 = [x1[0]+p[0], x1[1]+length]
				
		global sb
		self.serial = 'b' + str(sb) + str(ser)
		sb += 1
		self.par = p
		self.width = width = x2[0] - x1[0]
		self.hight = hight = x2[1] - x1[1]
		if width == p[0] or hight == p[0]:
			if width == p[0]:
				self.orientation = 'vertical'
				self.length = hight
			elif hight == p[0]:
				self.orientation = 'horizont'
				self.length = width
			else: print('Ошибка при вводе координат доски')
		elif width==p[1] or hight==p[1] and width>=p[1] and hight>=p[1]:
			if width == p[1]:
				self.orientation = 'vertical'
				self.length = hight
			elif hight == p[1]:
				self.orientation = 'horizont'
				self.length = width
			else: print('Ошибка при вводе координат доски')
		else:
			print('Ошибка при вводе координат объекта.')
			print(self.par)
			print(self.width, ' : ', self.hight)
				
		
class Window:
	def __init__(self, x1, x2=False, width=1200, hight=1700, b=[50, 150, 6000], space=626):
		self.x1 = x1
		if x2:
			self.x2 = x2
		else:
			self.x2 = x2 = [x1[0]+width, x1[1]+hight]
		self.width = x2[0] - x1[0]
		self.hight = x2[1] - x1[1]
		self.down_space = x1[1]
		
		self.wpb = wpb = int(self.width / space / 2)#Колич. доп. стоек окна
		self.left_left = x1[0]-b[0]*(wpb+2)
		self.left = x1[0]-b[0]*(wpb+1)
		self.right = x2[0]+b[0]*(wpb+1)
		self.right_right = x2[0]+b[0]*(wpb+2)
		self.win_hight = x2[1]+b[0]+b[1]
		

class Door:
	def __init__(self, x1, x2=False, width=980, hight=2071, b=[50, 150, 6000], space=626):
		self.x1 = x1
		if x2:
			self.x2 = x2
		else:
			self.x2 = x2 = [x1[0]+width, x1[1]+hight]
		self.width = x2[0] - x1[0]
		self.hight = x2[1] - x1[1]
		
		self.wpb = wpb = int(width / space / 2)#Колич. доп. стоек окна
		self.left_left = x1[0]-b[0]*(wpb+2)
		self.left = x1[0]-b[0]*(wpb+1)
		self.right = x2[0]+b[0]*(wpb+1)
		self.right_right = x2[0]+b[0]*(wpb+2)
		self.door_hight = x2[1]+b[0]+b[1]
		
	
class OSB:
	def __init__(self, x1, x2=False, ori='h', width=2500, hight=1250, is_cut=False, ser=''):
		self.x1 = x1
		if x2:
			self.x2 = x2
		else:
			if ori == 'h':
				self.x2 = x2 = [x1[0] + width, x1[1] + hight]
			else:
				self.x2 = x2 = [x1[0] + hight, x1[1] + width]
		global so
		if is_cut:
			self.serial = ser + '_o' + str(so)
			so += 1
		else:
			self.serial = 'o' + str(so)
			so += 1
		self.width = self.x2[0] - self.x1[0]
		self.hight = self.x2[1] - self.x1[1]
		self.is_cut = is_cut
		self.cut_zone = []
	def save(self):
		self.width = self.x2[0] - self.x1[0]
		self.hight = self.x2[1] - self.x1[1]
	def cut(self, x1, x2):
		self.cut_zone = [x1, x2]
		width = x2[0] - x1[0]
		hight = x2[1] - x1[1]
		return width, hight
		

def errors(width, hight, board, doors, windows, con):
	def print_er(text):
		print(text)
		exit()
	
	if con[0]:
		lc = board[1]
	else:
		lc = 0
	if con[1]:
		rc = board[1]
	else:
		rc = 0
	reserv = []
	if doors:
		for obj in doors:
			if obj.width < board[0] * 2:
				print_er('Ширина двери слишком маленькая.')
			if obj.hight < board[0] * 2:
				print_er('Высота двери слишком маленькая.')
			if obj.right_right > width - board[0] - rc:
				print_er('Дверь выходит за правую границу стены или расположена слишком близко к краю.')
			if obj.left_left < board[0] + lc:
				print_er('Дверь выходит за левую границу стены или расположена слишком близко к краю.')
			if obj.door_hight > hight - board[0] * 2:
				print_er('Дверь выходит за верхнюю границу стены или расположена слишком близко к верху.')
			if reserv:
				for i in reserv:
					if_in(x1=obj.x1, x2=obj.x2, y1=i.x1, y2=i.x2, pr=True, ex=True)
			reserv.append(obj)
			
	if windows:
		for obj in windows:
			if obj.width < board[0] * 2:
				print_er('Ширина окна слишком маленькая.')
			if obj.hight < board[0] * 2:
				print_er('Высота окна слишком маленькая.')
			if obj.down_space < board[0] * 2:
				print_er('Высота до подоконника слишком маленькая.')
			if obj.right_right > width - board[0] - rc:
				print_er('Окно выходит за правую границу стены или расположено слишком близко к краю.')
			if obj.left_left < board[0] + lc:
				print_er('Окно выходит за левую границу стены или расположено слишком близко к краю.')
			if obj.win_hight > hight - board[0] * 2:
				print_er('Окно выходит за верхнюю границу стены или расположено слишком близко к верху.')
			if reserv:
				for i in reserv:
					if_in(x1=obj.x1, x2=obj.x2, y1=i.x1, y2=i.x2, pr=True, ex=True)
			reserv.append(obj)


def if_in(x1, y1, y2, x2=False, pr=True, ex=True):
	def prin(text, ex=ex, pr=pr):
		if pr: print(text)
		if ex: exit()
		return False
		
	ld = lu = ru = rd = l = u = r = d = False
	if len(x1) != 2 and len(y1) != 2 and len(y2) != 2:
		if pr: prin('Неправильно введенный формат')
	if x2:
		if x1[0] <= y1[0] and x2[1] >= y2[1] and x2[0] >= y2[0] and x1[1] <= y1[1]:
			prin(f'Об. {1} находится поверх об. {2}')
			
		if x1[0] > y1[0] and x2[1] < y2[1] and x2[0] < y2[0] and x1[1] > y1[1]:
			prin(f'Об. {1} находится внутри об. {2}')
			
		if x1[0] > y1[0] and x1[0] < y2[0] and x1[1] < y1[1] and x2[1] > y2[1]:
			l = True
			prin(f'Левая грань об. {1} находит на об. {2}')

		if x2[0] > y1[0] and x2[0] < y2[0] and x1[1] < y1[1] and x2[1] > y2[1]:
			r = True
			prin(f'Правая грань об. {1} находит на об. {2}')

		if x2[1] > y1[1] and x2[1] < y2[1] and x1[0] < y1[0] and x2[0] > y2[0]:
			u = True
			prin(f'Верхняя грань об. {1} находит на об. {2}')

		if x1[1] > y1[1] and x1[1] < y2[1] and x1[0] < y1[0] and x2[0] > y2[0]:
			d = True
			prin(f'Нижняя грань об. {1} находит на об. {2}')
		
		if x1[0] > y1[0] and x1[0] < y2[0] and x1[1] > y1[1] and x1[1] < y2[1]:
			ld = True
		if x1[0] > y1[0] and x1[0] < y2[0] and x2[1] > y1[1] and x2[1] < y2[1]:
			lu = True
		if x2[0] > y1[0] and x2[0] < y2[0] and x2[1] > y1[1] and x2[1] < y2[1]:
			ru = True
		if x2[0] > y1[0] and x2[0] < y2[0] and x1[1] > y1[1] and x1[1] < y2[1]:
			rd = True
		
		if ld and lu:
			prin(f'Левая грань об. {1} внутри об. {2}')
		elif lu and ru:
			prin(f'Верхняя грань об. {1} внутри об. {2}')
		elif ru and rd:
			prin(f'Правая грань об. {1} внутри об. {2}')
		elif ld and rd:
			prin(f'Нижняя грань об. {1} внутри об. {2}')
			
		elif ld:
			prin(f'Левая нижняя точка об. {1} внутри об. {2}')
		elif lu:
			prin(f'Левая верхняя точка об. {1} внутри об. {2}')
		elif ru:
			prin(f'Правая верхняя точка об. {1} внутри об. {2}')
		elif rd:
			prin(f'Правая нижняя точка об. {1} внутри об. {2}')
		
	else:
		if x1[0] > y1[0] and x1[0] < y2[0] and x1[1] > y1[1] and x1[1] < y2[1]:
			prin('Находится внутри')
			return False
		else:
			print('Не внутри')
			return True


sw = 1


def compress_boards(brds, b=[50, 150, 6000]):
	
	class Wood:
		def __init__(self, cutline=3, b=[50, 150, 6000]):
			global sw
			self.serial = 'w' + str(sw)
			sw += 1
			self.cutline = cutline
			self.par = b
			self.boards = []
			self.free = b[2]
		def add_board(self, board):
			self.boards.append([board[0], board[1]])
			self.free -= board[0] + self.cutline

	boards, woods = [], []
	for board in brds:
		boards.append([board.length, board.serial])
	
	boards.sort(reverse=True)
	while True:
		if boards:
			wood = Wood(b=b)
			c = 0
			while True:
				if c >= len(boards):
					break
				if boards[c][0] <= wood.free:
					wood.add_board(boards.pop(c))
				else:
					c += 1
			woods.append(wood)
		else:
			break
	return woods


def make_vapor_barrier(wall, li=[1.6, 10]):
	x1, x2, pm, on = [0, 0], [0, wall.hight], li[0]*1000, li[1]*10
	if not wall.lc: x1[0] = 0 + wall.board[1]
	else: x1[0] = 0 - on
	if not wall.rc: x2[0] = wall.width - wall.board[1]
	else: x2[0] = wall.width + on
	level = 0
	lvl = 0
	while level+on < wall.hight:
		level += pm - on
		lvl += 1
	return round((x2[0]-x1[0])/1000*lvl, 2)


def make_wind_protection(wall, li=[1.6, 20]):
	x1, x2 = [0-wall.lc, 0-wall.lvl[0]], [wall.width+wall.rc, wall.hight+wall.lvl[1]]
	pm = li[0]*1000
	on = li[1]*10
	level = 0
	lvl = 0
	while level+on < wall.hight:
		level += pm - on
		lvl += 1
	return round((x2[0]-x1[0])/1000*lvl, 2)


def nails_osb(bs, sp=150):
	sum_l = 0
	for i in bs:
		sum_l += i.length
	return int(sum_l/sp)


def rail(wall):
	r = []
	return r
