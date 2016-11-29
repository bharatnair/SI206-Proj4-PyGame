import random
import sys

from pygame import *
from pygame.sprite import *
from random import *

import pygame
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, \
	K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL, K_RETURN, FULLSCREEN
pygame.init()

x_window_max = 800
y_window_max = 600
top_buffer = 20
bottom_buffer = y_window_max-20
left_buffer = 20
right_buffer = x_window_max-20

LEFT, RIGHT, UP, DOWN = 0, 1, 3, 4
START, STOP = 0, 1

f = pygame.font.SysFont("monospace", 25)
screen = pygame.display.set_mode((x_window_max, y_window_max), DOUBLEBUF)
pygame.display.set_caption('Survive!')

everything = pygame.sprite.Group()

time_limit = 10
lives_limit = 3

pygame.font.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

class companionSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(companionSprite, self).__init__()
        self.image = pygame.image.load("companion.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        randX = randint(50, x_window_max-50)
        randY = randint(50, y_window_max-50)
        self.rect.center = (randX,randY)

    # def update(self):
    # 	screen.blit
        
    def hit(self, target):
        return self.rect.colliderect(target)

class CellSprite(pygame.sprite.Sprite):
	def __init__(self):
		super(CellSprite, self).__init__()
		self.image = pygame.image.load("hero.bmp").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (x_window_max/2, y_window_max/2 - 20)
		self.dx = self.dy = 0
		self.firing = self.shot = False
		self.health = lives_limit
		self.score = 0

		# self.groups = [groups]

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

class intialText(pygame.sprite.Sprite):
	def __init__(self):
		it_1 = f.render("Go Pickup Your Companion Cell.", False, (250,250,250))
		it_2 = f.render("Move With The Arrow Keys.", False, (250,250,250))

	def update(self):
		it_1 = f.render("Go Pickup Your Companion Cell.", False, (250,250,250))
		it_2 = f.render("Move With The Arrow Keys.", False, (250,250,250))
		screen.blit(it_1, (30, y_window_max-50))
		screen.blit(it_2, (30, y_window_max-80))

game_over = False
def pickup():
	companion = companionSprite()
	ship = CellSprite()
	ini = intialText()
	sprites = RenderPlain(companion, ship)

	while True:
		# pygame.clock.tick(30)
		
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

			if companion.hit(ship):
				print ("they collided!")
				break
		screen.fill((0,0,0))
		sprites.update()
		ini.update()
		sprites.draw(screen)
		display.update()
		
	pygame.quit()
	quit()

pickup()

