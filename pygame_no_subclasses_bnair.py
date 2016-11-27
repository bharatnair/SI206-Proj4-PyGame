import random
import sys
from pygame import *
from pygame.sprite import *
from random import *
import pygame
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, \
	K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL, K_RETURN, FULLSCREEN, K_q, K_r

# pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

x_window_max = 800
y_window_max = 600

top_buffer = (0.05*y_window_max)
bottom_buffer = y_window_max-(0.05*y_window_max)
left_buffer = (0.05*y_window_max)
right_buffer = x_window_max-(0.05*y_window_max)

LEFT, RIGHT, UP, DOWN = 0, 1, 3, 4
START, STOP = 0, 1

try:
	f = pygame.font.SysFont("trebuchetms", 25)
except:
	f = pygame.font.SysFont("monospace", 25)

screen = pygame.display.set_mode((x_window_max, y_window_max), DOUBLEBUF)
pygame.display.set_caption('Protect Your Companion Cell!')

everything = pygame.sprite.Group()

time_limit = 10
lives_limit = 3

class companionSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(companionSprite, self).__init__()
        self.image = pygame.image.load("companion.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        randX = randint(50, x_window_max-50)
        randY = randint(50, y_window_max-90)
        self.rect.center = (randX,randY)
        
    def hit(self, target):
        return self.rect.colliderect(target)

class pickupCellSprite(pygame.sprite.Sprite):
	def __init__(self):
		super(pickupCellSprite, self).__init__()
		self.image = pygame.image.load("hero.bmp").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (x_window_max/2, y_window_max/2 - 20)
		self.dx = self.dy = 0
		self.health = lives_limit

		self.autopilot = False
		self.in_position = False
		self.velocity = 2

	def update(self):
		x, y = self.rect.center
		ndx = x + self.dx
		ndy =  y + self.dy

		if not self.autopilot:
			if (ndy > bottom_buffer):
				ndy = bottom_buffer
			if (ndy < top_buffer):
				ndy = top_buffer
			if (ndx > right_buffer):
				ndx = right_buffer
			if (ndx < left_buffer):
				ndx = left_buffer
			self.rect.center = ndx, ndy
		else:
			if not self.in_position:
				if x != x_window_max/2:
					x += (abs(x_window_max/2 - x)/(x_window_max/2 - x)) * 2
				if y != y_window_max - 100:
					y += (abs(y_window_max - 100 - y)/(y_window_max - 100 - y)) * 2

				if x == x_window_max/2 and y == y_window_max - 100:
					self.in_position = True
			else:
				y -= self.velocity
				self.velocity *= 1.5
				if y <= 0:
					y = -30
			self.rect.center = x, y

	def move(self, direction, operation):
		v = 5
		if operation == START:
			if direction in (UP, DOWN):
				self.dy = {UP: -v,
						   DOWN: v}[direction]

			if direction in (LEFT, RIGHT):
				self.dx = {LEFT: -v,
						   RIGHT: v}[direction]

		if operation == STOP:
			if direction in (UP, DOWN):
				self.dy = 0
			if direction in (LEFT, RIGHT):
				self.dx = 0

class intialText(pygame.sprite.Sprite):
	def __init__(self):
		it_1 = f.render("Go Pickup Your Companion Cell.", False, (250,250,250))
		it_2 = f.render("Move With The Arrow Keys.", False, (250,250,250))

	def update(self):
		it_1 = f.render("Go Pickup Your Companion Cell.", False, (250,250,250))
		it_2 = f.render("Move With The Arrow Keys.", False, (250,250,250))
		screen.blit(it_1, (30, y_window_max-50))
		screen.blit(it_2, (30, y_window_max-80))

class lifeCountAndTimer(pygame.sprite.Sprite):
	def __init__(self):
		tC_t = f.render("Survive for " + str(time_limit) + " seconds!", False, (250,250,250))
		lC_t = f.render(str(lives_limit) + " lives left", False, (250,250,250))

	def update(self, seconds, health):
		screen.fill((0,0,0))
		if seconds<(0.25*time_limit):
			tC_t = f.render("Protect Your Companion for " + str(time_limit) + " seconds!", False, (0,250,250))
		elif seconds>=(0.25*time_limit) and seconds<(0.7*time_limit):
			tC_t = f.render("Survive!", False, (0,250,250))
		elif seconds>=(0.7*time_limit):
			tC_t = f.render("Almost there!", False, (0,250,250))
		screen.blit(tC_t, (30, y_window_max-50))

		lC_t = f.render("Lives left : " + str(health), False, (250,250,250))
		screen.blit(lC_t, (30, y_window_max-80))

class EnemySprite(pygame.sprite.Sprite):
	def __init__(self, x_pos, groups):
		super(EnemySprite, self).__init__()
		self.image = pygame.image.load("enemy.bmp").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (x_pos, 0)
		self.velocity = randint(6, 15)
		self.add(groups)

	def update(self):
		x, y = self.rect.center
		if y > y_window_max:
			x, y = randint(0, x_window_max), 0
			self.velocity = randint(6, 12)
		else:
			x, y = x, y + self.velocity

		self.rect.center = x, y

class CellSprite(pygame.sprite.Sprite):
	def __init__(self, groups):
		super(CellSprite, self).__init__()
		self.image = pygame.image.load("heroAndCompanion.bmp").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (0.5*x_window_max, 0.7*y_window_max)
		self.dx = self.dy = 0
		self.health = lives_limit
		self.groups = [groups]
		self.autopilot = False
		self.in_position = False
		self.velocity = 2

	def update(self):
		x, y = self.rect.center
		ndx = x + self.dx
		ndy =  y + self.dy
		
		if not self.autopilot:
			# Handle movement
			if (ndy > bottom_buffer):
				ndy = bottom_buffer
			if (ndy < top_buffer):
				ndy = top_buffer
			if (ndx > right_buffer):
				ndx = right_buffer
			if (ndx < left_buffer):
				ndx = left_buffer
			self.rect.center = ndx, ndy
		else:
			if not self.in_position:
				if x != x_window_max/2:
					x += (abs(x_window_max/2 - x)/(x_window_max/2 - x)) * 2
				if y != y_window_max - 100:
					y += (abs(y_window_max - 100 - y)/(y_window_max - 100 - y)) * 2

				if x == x_window_max/2 and y == y_window_max - 100:
					self.in_position = True
			else:
				y -= self.velocity
				self.velocity *= 1.5
				if y <= 0:
					y = -30
			self.rect.center = x, y

	def move(self, direction, operation):
		v = 10
		if operation == START:
			if direction in (UP, DOWN):
				self.dy = {UP: -v,
						   DOWN: v}[direction]

			if direction in (LEFT, RIGHT):
				self.dx = {LEFT: -v,
						   RIGHT: v}[direction]

		if operation == STOP:
			if direction in (UP, DOWN):
				self.dy = 0
			if direction in (LEFT, RIGHT):
				self.dx = 0

class pickupCellSprite(CellSprite):
	def __init__(self):
		# super(pickupCellSprite, self).__init__(groups)
		CellSprite.__init__(groups)
		self.image = pygame.image.load("hero.bmp").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (x_window_max/2, y_window_max/2 - 20)
		self.dx = self.dy = 0
		self.health = lives_limit

		self.autopilot = False
		self.in_position = False
		self.velocity = 2

def endgameFunc(seconds, health):
	screen.fill((0,0,0))
	
	if seconds >= time_limit:
		endGame_t_1 = f.render("You Saved Your Companion!", False, (35,180,35))
		endGame_t_2 = f.render("You Won!", False, (35,180,35))
		# screen.blit(endGame_t, (x_window_max/2, y_window_max/2))
		pygame.mixer.Sound("game_win_sound.wav").play()
		print ("\nCongratulations! You Won!\n")
	
	if health <= 0:
		endGame_t_1 = f.render("You Couldn't Save Your Companion.", False, (160,35,35))
		endGame_t_2 = f.render("You Lost.", False, (160,35,35))
		# screen.blit(endGame_t, (x_window_max/2, y_window_max/2))
		pygame.mixer.Sound("game_over_sound.wav").play()
		print ("\nOh, No! You Lost!\n")
	
	gameExit = False
	
	while gameExit == False:
		screen.fill((0,0,0))
		screen.blit(endGame_t_1, (30, y_window_max-110))
		screen.blit(endGame_t_2, (30, y_window_max-80))
		endOption_t = f.render("Press Any Key To Quit.", False, (240,225,65))
		screen.blit(endOption_t, (30, y_window_max-50))
		
		for event in pygame.event.get():
			if (event.type == QUIT) or (event.type == KEYDOWN):
				gameExit = True
				break

		pygame.display.update()			
	
	pygame.quit()
	quit()

def main():
	game_over = False
	
	enemies = pygame.sprite.Group()

	empty = pygame.Surface((x_window_max, y_window_max))
	clock = pygame.time.Clock()

	ship = CellSprite(everything)
	ship.add(everything)

	for i in range(10):
		pos = randint(0, x_window_max)
		EnemySprite(pos, [everything, enemies])

	counterz = lifeCountAndTimer()

	start_ticks=pygame.time.get_ticks()
	
	while True:
		seconds=(pygame.time.get_ticks()-start_ticks)/1000
		clock.tick(30)
		
		for event in pygame.event.get():
			if event.type == QUIT or (
					event.type == KEYDOWN and event.key == K_ESCAPE):
				sys.exit()
			if not game_over:
				if event.type == KEYDOWN:
					if event.key == K_DOWN:
						ship.move(DOWN, START)
					if event.key == K_LEFT:
						ship.move(LEFT, START)
					if event.key == K_RIGHT:
						ship.move(RIGHT, START)
					if event.key == K_UP:
						ship.move(UP, START)
				if event.type == KEYUP:
					if event.key == K_DOWN:
						ship.move(DOWN, STOP)
					if event.key == K_LEFT:
						ship.move(LEFT, STOP)
					if event.key == K_RIGHT:
						ship.move(RIGHT, STOP)
					if event.key == K_UP:
						ship.move(UP, STOP)

		# Checking for collision
		hit_ships = pygame.sprite.spritecollide(ship, enemies, True)
		for i in hit_ships:
			ship.health -= 1
			pygame.mixer.Sound("game_hit_sound_1.wav").play()

		# Checking for bad game over
		if ship.health == 0:
			game_over = True

		if len(enemies) < 20 and not game_over:
			pos = randint(0, x_window_max)
			EnemySprite(pos, [everything, enemies])

		# Checking for good game over
		if seconds >= time_limit:
			game_over = True


		if game_over == True:
			endgameFunc(seconds, ship.health)
			sys.exit()

		# Update sprites
		everything.clear(screen, empty)
		everything.update()
		everything.draw(screen)
		pygame.display.flip()
		counterz.update(seconds, ship.health)

def pickup():
	game_done = False
	companion = companionSprite()
	ship = pickupCellSprite()
	ini = intialText()

	sprites = RenderPlain(companion, ship)
	while True:
		# pygame.clock.tick(30)
		for event in pygame.event.get():
			if event.type == QUIT or (
					event.type == KEYDOWN and event.key == K_ESCAPE):
				sys.exit()
			if not game_done:
				if event.type == KEYDOWN:
					if event.key == K_DOWN:
						ship.move(DOWN, START)
					if event.key == K_LEFT:
						ship.move(LEFT, START)
					if event.key == K_RIGHT:
						ship.move(RIGHT, START)
					if event.key == K_UP:
						ship.move(UP, START)
				if event.type == KEYUP:
					if event.key == K_DOWN:
						ship.move(DOWN, STOP)
					if event.key == K_LEFT:
						ship.move(LEFT, STOP)
					if event.key == K_RIGHT:
						ship.move(RIGHT, STOP)
					if event.key == K_UP:
						ship.move(UP, STOP)

			if companion.hit(ship):
				pygame.mixer.Sound("pickup.wav").play()
				main()
		
		screen.fill((0,0,0))
		sprites.update()
		ini.update()
		sprites.draw(screen)
		display.update()
	pygame.quit()
	quit()

pickup()