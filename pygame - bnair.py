#basic code and stuff

import random
import sys

import pygame
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, \
    K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL, K_RETURN, FULLSCREEN
pygame.init()

x_window_max = 800
y_window_max = 600

LEFT, RIGHT, UP, DOWN = 0, 1, 3, 4
START, STOP = 0, 1

everything = pygame.sprite.Group()

class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, x_pos, groups):
        super(EnemySprite, self).__init__()
        self.image = pygame.image.load("cc.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, 0)

        self.velocity = random.randint(6, 15)

        self.add(groups)

    def update(self):
        x, y = self.rect.center

        if y > y_window_max:
            x, y = random.randint(0, x_window_max), 0
            self.velocity = random.randint(6, 12)
        else:
            x, y = x, y + self.velocity

        self.rect.center = x, y


class CellSprite(pygame.sprite.Sprite):
    def __init__(self, groups):
        super(CellSprite, self).__init__()
        self.image = pygame.image.load("tt.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x_window_max/2, y_window_max/2 - 80)
        self.dx = self.dy = 0
        self.firing = self.shot = False
        self.health = 100
        self.score = 0

        self.groups = [groups]

        self.autopilot = False
        self.in_position = False
        self.velocity = 2

    def update(self):
        x, y = self.rect.center

        if not self.autopilot:
            # Handle movement
            self.rect.center = x + self.dx, y + self.dy

            if self.health < 0:
                self.kill()
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


def main():
    game_over = False

    pygame.font.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((x_window_max, y_window_max), DOUBLEBUF)
    enemies = pygame.sprite.Group()

    f = pygame.font.SysFont("monospace", 25)

    empty = pygame.Surface((x_window_max, y_window_max))
    clock = pygame.time.Clock()

    # stars = create_starfield(everything)

    ship = CellSprite(everything)
    ship.add(everything)

    # status = StatusSprite(ship, everything)
    credits_timer = 150

    for i in range(10):
        pos = random.randint(0, x_window_max)
        EnemySprite(pos, [everything, enemies])

    # # Get some music
    # if pygame.mixer.get_init():
    #     pygame.mixer.music.load("DST-AngryMod.mp3")
    #     pygame.mixer.music.set_volume(0.8)
    #     pygame.mixer.music.play(-1)

    start_ticks=pygame.time.get_ticks()
    while game_over == False:
        seconds=(pygame.time.get_ticks()-start_ticks)/1000
        clock.tick(30)
        t = f.render("Seconds = " + str(int(10-seconds)), False, (250,250,250))
        screen.blit(t, (320, 0))  
        # Check for input
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

        # Check for impact
        hit_ships = pygame.sprite.spritecollide(ship, enemies, True)
        for i in hit_ships:
            ship.health -= 50

        if ship.health == 0:
            game_over = True
            sys.exit()

        if len(enemies) < 20 and not game_over:
            pos = random.randint(0, x_window_max)
            EnemySprite(pos, [everything, enemies])

        # Check for game over
        if seconds > 10:
            game_over = True
            sys.exit()

        # Update sprites
        everything.clear(screen, empty)
        everything.update()
        everything.draw(screen)
        pygame.display.flip()
    
    pygame.quit()
    quit()

if __name__ == '__main__':
    main()
