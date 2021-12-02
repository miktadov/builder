from PIL import Image, ImageDraw


def estimate(wall, show=True):
	txt = []
	txt.append(f'Параметры стены:\nвысота: {wall.hight} \nширина: {wall.width}\n')
	if wall.doors:
		last = len(wall.doors)
		if last == 1:
			la = 'ь'
		elif last < 5:
			la = 'и'
		else:
			la = 'ей'
		txt.append(f'{last} двер{la}\n')
	if wall.windows:
		last = len(wall.windows)
		if last == 1:
			la = 'но'
		elif last < 5:
			la = 'на'
		else:
			la = 'ок'
		txt.append(f'{last} ок{la}\n')

	last = int(str(len(wall.woods))[-1])
	if last == 1:
		la = 'ка'
	elif last < 5 and last != 0:
		la = 'ки'
	else:
		la = 'ок'
	txt.append(f'\nНа данную стену уйдет:\n{len(wall.woods)} дос{la} {wall.board[0]}x{wall.board[1]}x{wall.board[2]}')
	last = len(wall.osb)
	if last == 1 or last == 101:
		la = 'а'
	elif last < 5 or last > 101 and last < 105:
		la = 'ы'
	else:
		la = ''
	txt.append(f'\n{last} ОСБ плит{la}')

	if wall.wata50:
		txt.append(f'\n{wall.wata50} м² 50мм утеплителя')
	if wall.wata100:
		txt.append(f'\n{wall.wata100} м² 100мм утеплителя')

	txt.append(f'\n{wall.vapor_barrier} м.пог пароизоляции')
	txt.append(f'\n{wall.wind_protection} м.пог ветро-гидро изоляции')
	txt.append(f'\n{wall.nails} шт. гвоздей')

	if show is True:
		for row in txt:
			print(row)

	text = open("estimate.txt", "w", encoding="UTF-8")
	for row in txt:
		text.write(row)
	text.close()


def make_image(wall, sp=[50, 50, 50, 50]):
#	def line(x1, x2, pos='l'):
#		idraw = ImageDraw.Draw(tatras)
#		text = "High Tatras"
#		font = ImageFont.truetype("arial.ttf", size=18)
#		idraw.text((10, 10), text, font=font)
#		tatras.save('tatras_watermarked.png')
#		return 
	print('\nОтрисовка проекта...')
	wi, hi = wall.width, wall.hight
	l, u, r, d = sp[0], sp[1], sp[2], sp[3]
	img = Image.new('RGBA', (wi+l+r, hi+d+u), 'white')
	idraw = ImageDraw.Draw(img)
	
	for b in wall.bs:
		idraw.rectangle([b.x1[0]+l, hi-b.x1[1]+u, b.x2[0]+l, hi-b.x2[1]+u], outline='black', width=2, fill='lightgrey')
	
	for b in wall.osb+wall.osb_cuts:
		idraw.rectangle([b.x1[0]+l, hi-b.x1[1]+u, b.x2[0]+l, hi-b.x2[1]+u], outline='red', width=3)
	
	width, height = img.size
	new_width  = 2000 # ширина
	new_height = int(new_width * height / width)
	img = img.resize((new_width, new_height), Image.ANTIALIAS)
	
	img.save('project.png')
	img.show()

	