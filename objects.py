import pygame
import random
SCREEN = WIDTH, HEIGHT = 530 , 860
pygame.mixer.init()
class Background():
	def __init__(self, win):
		self.win = win

		self.image = pygame.image.load('Assets/bg.png')
		self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
		self.rect = self.image.get_rect()

		self.reset()
		self.move = True

	def update(self, speed):
		if self.move:
			self.y1 += speed
			self.y2 += speed

			if self.y1 >= HEIGHT:
				self.y1 = -HEIGHT
			if self.y2 >= HEIGHT:
				self.y2 = -HEIGHT

		self.win.blit(self.image, (self.x,self.y1))
		self.win.blit(self.image, (self.x,self.y2))

	def reset(self):
		self.x = 0
		self.y1 = 0
		self.y2 = -HEIGHT

class Player:
	def __init__(self, x, y):

		self.image_list = []
		for i in range(2):
			img = pygame.image.load(f'Assets/player{i+1}.png')
			img = pygame.transform.scale(img, (100, 86))
			self.image_list.append(img)

		self.x, self.y = x, y
		self.reset(self.x, self.y)

	def reset(self, x, y):
		self.index = 0
		self.image = self.image_list[self.index]
		self.rect = self.image.get_rect(center=(x, y))

		self.counter = 0
		self.speed = 4
		self.health = 1000
		self.fuel = 500
		self.powerup = 0
		self.superweapon = 0
		self.alive = True
		self.width = self.image.get_width()
		self.height = self.image.get_height()

	def update(self, moving_left, moving_right, moving_up, moving_down, explosion_group):
		if self.alive:
			if moving_left and self.rect.x > 2:
				self.rect.x -= self.speed

			if moving_right and self.rect.x < WIDTH - self.width:
				self.rect.x += self.speed

			if moving_up and self.rect.y > 2:
				self.rect.y -= self.speed

			if moving_down and self.rect.y < HEIGHT - self.height:
				self.rect.y += self.speed

			if self.health <= 0:
				x, y = self.rect.center
				explosion = Explosion(x, y, 2)
				explosion_group.add(explosion)

				self.alive = False

			self.counter += 1
			if self.counter >= 20:
				self.index = (self.index + 1) % len(self.image_list)
				self.image = self.image_list[self.index]
				self.counter = 0

	def draw(self, win):
		if self.alive:
			win.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y, type_):
		super(Enemy, self).__init__()

		self.type = type_
		self.image_list = []
		for i in range(2):
			if type_ == 1:
				img = pygame.image.load(f'Assets/Enemies/enemy1-{i+1}.png')
				self.speed = 2
				self.health = 200
				w, h = img.get_width(), img.get_height()
				height = (100 * h) // w
				img = pygame.transform.scale(img, (100, height))
			if type_ == 2:
				img = pygame.image.load(f'Assets/Enemies/enemy2-{i+1}.png')
				self.speed = 2.5
				self.health = 250
				w, h = img.get_width(), img.get_height()
				height = (100 * h) // w
				img = pygame.transform.scale(img, (100, height))
			if type_ == 3:
				img = pygame.image.load(f'Assets/Enemies/enemy3-{i+1}.png')
				self.speed = 3
				self.health = 400
				w, h = img.get_width(), img.get_height()
				height = (100 * h) // w
				img = pygame.transform.scale(img, (100, height))
			if type_ == 4:
				img = pygame.image.load(f'Assets/Enemies/enemy4-{i+1}.png')
				self.speed = 1.5
				self.health = 10000
				w, h = img.get_width(), img.get_height()
				height = (100 * h) // w
				img = pygame.transform.scale(img, (200, height*2))
				
			self.image_list.append(img)

		self.index = 0
		self.image = self.image_list[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.frame_dict = {1:3, 2:3, 3:3, 4:5, 5:4}
		self.frame_fps = self.frame_dict[type_]

		self.counter = 0
		self.movecounter = 240
		self.bullet_counter = 0
		self.move_index = 1
		
		

		if self.type in (1,2,3):
			self.fx = pygame.mixer.Sound('Sounds/plane.mp3')
			self.fx.set_volume(0.001)
		elif self.type in (4, 5):
			self.fx = pygame.mixer.Sound('Sounds/chopper.mp3')
			self.fx.set_volume(0.001)

		self.fx.play(-1)

	def shoot(self, enemy_bullet_group):
		if self.type == 1:
			x = self.rect.centerx
			y = self.rect.bottom
			b = Bullet(x, y, 1)
			enemy_bullet_group.add(b)
		elif self.type == 2:
			x = self.rect.left
			y = self.rect.bottom
			b = Bullet(x, y, 2)
			enemy_bullet_group.add(b)
			x = self.rect.right
			y = self.rect.bottom
			b = Bullet(x, y, 2)
			enemy_bullet_group.add(b)
		elif self.type == 3:
			x = self.rect.left
			y = self.rect.bottom
			b = Bullet(x, y, 2)
			enemy_bullet_group.add(b)
			x = self.rect.right
			y = self.rect.bottom
			b = Bullet(x, y, 2)
			enemy_bullet_group.add(b)
			x = self.rect.centerx
			y = self.rect.bottom
			b = Bullet(x, y, 3)
			enemy_bullet_group.add(b)
		elif self.type == 4:
			x = self.rect.left
			y = self.rect.bottom
			b = Bullet(x, y, 2)
			enemy_bullet_group.add(b)
			x = self.rect.right
			y = self.rect.bottom
			b = Bullet(x, y, 2)
			enemy_bullet_group.add(b)
			x = self.rect.centerx
			y = self.rect.bottom
			b = Bullet(x-40, y, 3)
			enemy_bullet_group.add(b)
			x = self.rect.centerx
			y = self.rect.bottom
			b = Bullet(x+40, y, 3)
			enemy_bullet_group.add(b)
		


	def update(self, enemy_bullet_group, explosion_group):
		
		if self.movecounter == 0:
			self.move_index = random.randint(1, 8)
			self.movecounter = 240
		else:
			self.movecounter -= 1
		
		if self.type in (1,2,3):
			if self.move_index == 1:
				self.rect.y += self.speed
			elif self.move_index == 2:
				self.rect.y -= self.speed
				self.rect.x -= self.speed
			elif self.move_index == 3:
				self.rect.x += self.speed
			elif self.move_index == 4:
				self.rect.y += self.speed
				self.rect.x -= self.speed
			elif self.move_index == 5:
				self.rect.y += self.speed
				self.rect.x += self.speed
			elif self.move_index == 6:
				self.rect.x -= self.speed
			elif self.move_index == 7:
				self.rect.y -= self.speed
				self.rect.x += self.speed
			elif self.move_index == 8:
				self.rect.y -= self.speed
			if self.rect.x <= -110:
				self.rect.x = -110
			if self.rect.x >= 530:
				self.rect.x = 530
			if self.rect.y <= -10:
				self.rect.y = -10
			if self.rect.y >= 300:
				self.rect.y = 300

		elif self.type == 4:
			if self.move_index == 1:
				self.rect.y += self.speed
			elif self.move_index == 2:
				self.rect.y -= self.speed
				self.rect.x -= self.speed
			elif self.move_index == 3:
				self.rect.x += self.speed
			elif self.move_index == 4:
				self.rect.y += self.speed
				self.rect.x -= self.speed
			elif self.move_index == 5:
				self.rect.y += self.speed
				self.rect.x += self.speed
			elif self.move_index == 6:
				self.rect.x -= self.speed
			elif self.move_index == 7:
				self.rect.y -= self.speed
				self.rect.x += self.speed
			elif self.move_index == 8:
				self.rect.y -= self.speed
			if self.rect.x <= -210:
				self.rect.x = -210
			if self.rect.x >= 530:
				self.rect.x = 530
			if self.rect.y <= -10:
				self.rect.y = -10
			if self.rect.y >= 300:
				self.rect.y = 300

		if self.health <= 0:
			x, y = self.rect.center
			explosion = Explosion(x, y, 2)
			explosion_group.add(explosion)

			self.fx.stop()
			self.kill()

		self.bullet_counter += 1
		if self.bullet_counter >= 60:
			self.shoot(enemy_bullet_group)
			self.bullet_counter = 0

		self.counter += 1
		if self.counter >= self.frame_fps*10:
			self.index = (self.index + 1) % len(self.image_list)
			self.image = self.image_list[self.index]
			self.counter = 0

	def draw(self, win):
		win.blit(self.image, self.rect)
		


class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, type_, dy=None ,dx=None):
		super(Bullet, self).__init__()

		self.dx = dx
		self.dy = dy
		self.type = type_
		#敵人子彈型態
		if type_ == 1:
			rand = random.randint(1,2)
			if rand == 1:
				self.image = pygame.image.load('Assets/Bullets/HW1.png')
			else:
				self.image = pygame.image.load('Assets/Bullets/HW1(1).png')
			self.image = pygame.transform.scale(self.image, (20, 50))
			self.speed = 5
		if type_ == 2:
			rand = random.randint(1,2)
			if rand == 1:
				self.image = pygame.image.load('Assets/Bullets/HW2.png')
			else:
				self.image = pygame.image.load('Assets/Bullets/HW2(1).png')
			self.image = pygame.transform.scale(self.image, (20, 50))
			self.speed = 5
		if type_ == 3:
			rand = random.randint(1,2)
			if rand == 1:
				self.image = pygame.image.load('Assets/Bullets/Exam.png')
			else:
				self.image = pygame.image.load('Assets/Bullets/Exam(1).png')
			self.image = pygame.transform.scale(self.image, (23, 53))
			self.speed = 6
		if type_ == 4:
			self.image = pygame.image.load('Assets/Bullets/Final_project.png')
			self.image = pygame.transform.scale(self.image, (20, 20))
			self.speed = 7
		#玩家子彈型態
		if type_ == 6:
			rand = random.randint(1,2)
			if rand == 1:
				self.image = pygame.image.load('Assets/Bullets/6.png')
			else:
				self.image = pygame.image.load('Assets/Bullets/6(1).png')
			self.image = pygame.transform.scale(self.image, (25, 55))
			self.speed = -5
		if type_ == 7:
			rand = random.randint(1,2)
			if rand == 1:
				self.image = pygame.image.load('Assets/Bullets/7.png')
			else:
				self.image = pygame.image.load('Assets/Bullets/7(1).png')
			self.image = pygame.transform.scale(self.image, (25, 55))
			self.speed = -5.5
		if type_ == 8:
			rand = random.randint(1,2)
			if rand == 1:
				self.image = pygame.image.load('Assets/Bullets/8.png')
			else:
				self.image = pygame.image.load('Assets/Bullets/8(1).png')
			self.image = pygame.transform.scale(self.image, (35, 100))
			self.speed = -5
		#超級武器
		if type_ == 10:
			self.image = pygame.image.load('Assets/Bullets/10.png') 
			self.image = pygame.transform.scale(self.image, (25, 25))
			self.speed = 0

		self.rect = self.image.get_rect(center=(x, y))
	

		if self.dx == None:
			self.dx = 0
		if self.dy == None:
			self.dy = 0

		self.damage_dict = {1:5, 2:10, 3:15, 4:25, 5: 25, 6:20, 7:25, 8:30, 10:400}
		self.damage = self.damage_dict[type_]
		


	def update(self):
		if self.type == 10:
			self.rect.x += self.dx
			self.rect.y += self.dy
		else:	
			self.rect.x += self.dx
			self.rect.y += self.speed
		if self.rect.bottom <= 0:
			self.kill()
		if self.rect.top >= HEIGHT:
			self.kill()

	def draw(self, win):
		win.blit(self.image, self.rect)


class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, type_):
		super(Explosion, self).__init__()


		self.img_list = []
		if type_ == 1:
			self.length = 3
		elif type_ == 2:
			self.length = 8

		for i in range(self.length):
			img = pygame.image.load(f'Assets/Explosion{type_}/{i+1}.png')
			w, h = img.get_size()
			width = int(w * 0.40)
			height = int(w * 0.40)
			img = pygame.transform.scale(img, (width, height))
			self.img_list.append(img)

		self.index = 0
		self.image = self.img_list[self.index]
		self.rect = self.image.get_rect(center=(x, y))

		self.counter = 0

	def update(self):
		self.counter += 1
		if self.counter >= 3:
			self.index += 1
			if self.index >= self.length:
				self.kill()
			else:
				self.image = self.img_list[self.index]
				self.counter = 0

		
	def draw(self, win):
		win.blit(self.image, self.rect)


class Fuel(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Fuel, self).__init__()

		self.image = pygame.image.load('Assets/fuel.png')
		self.image = pygame.transform.scale(self.image, (50, 60))
		self.rect = self.image.get_rect(center=(x, y))

	def update(self):
		self.rect.y += 1
		if self.rect.top >= HEIGHT:
			self.kill()

	def draw(self, win):
		win.blit(self.image, self.rect)

class Powerup(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Powerup, self).__init__()

		self.image = pygame.image.load('Assets/powerup.png')
		self.image = pygame.transform.scale(self.image, (50, 50))
		self.rect = self.image.get_rect(center=(x, y))

	def update(self):
		self.rect.y += 1
		if self.rect.top >= HEIGHT:
			self.kill()

	def draw(self, win):
		win.blit(self.image, self.rect)

class Life(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Life, self).__init__()

		self.image = pygame.image.load('Assets/life.png')
		self.image = pygame.transform.scale(self.image, (50, 50))
		self.rect = self.image.get_rect(center=(x, y))

	def update(self):
		self.rect.y += 1
		if self.rect.top >= HEIGHT:
			self.kill()

	def draw(self, win):
		win.blit(self.image, self.rect)

class Superweapon(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Superweapon, self).__init__()

		self.image = pygame.image.load('Assets/Superweapon.png')
		self.image = pygame.transform.scale(self.image, (50, 40))
		self.rect = self.image.get_rect(center=(x, y))

	def update(self):
		self.rect.y += 1
		if self.rect.top >= HEIGHT:
			self.kill()

	def draw(self, win):
		win.blit(self.image, self.rect)


class Button(pygame.sprite.Sprite):
	def __init__(self, img, scale, x, y):
		super(Button, self).__init__()
		
		self.scale = scale
		self.image = pygame.transform.scale(img, self.scale)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.clicked = False

	def update_image(self, img):
		self.image = pygame.transform.scale(img, self.scale)

	def draw(self, win):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True

			if not pygame.mouse.get_pressed()[0]:
				self.clicked = False

		win.blit(self.image, self.rect)
		return action

class Message:
	def __init__(self, x, y, size, text, font, color, win):
		self.win = win
		self.color = color
		self.x, self.y = x, y
		if not font:
			self.font = pygame.font.SysFont("Verdana", size)
			anti_alias = True
		else:
			self.font = pygame.font.Font(font, size)
			anti_alias = False
		self.image = self.font.render(text, anti_alias, color)
		self.rect = self.image.get_rect(center=(x,y))
		self.shadow = self.font.render(text, anti_alias, (54,69,79))
		self.shadow_rect = self.image.get_rect(center=(x+2,y+2))
		
	def update(self, text=None, shadow=True):
		if text:
			self.image = self.font.render(f"{text}", False, self.color)
			self.rect = self.image.get_rect(center=(self.x,self.y))
			self.shadow = self.font.render(f"{text}", False, (54,69,79))
			self.shadow_rect = self.image.get_rect(center=(self.x+2,self.y+2))
		if shadow:
			self.win.blit(self.shadow, self.shadow_rect)
		self.win.blit(self.image, self.rect)

class BlinkingText(Message):
	def __init__(self, x, y, size, text, font, color, win):
		super(BlinkingText, self).__init__(x, y, size, text, font, color, win)
		self.index = 0
		self.show = True

	def update(self):
		self.index += 1
		if self.index % 40 == 0:
			self.show = not self.show

		if self.show:
			self.win.blit(self.image, self.rect)