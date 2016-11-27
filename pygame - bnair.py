#just screw it tbh man.
##
#how do i get the endgame screeen to trigger?
    #how do i get to allow clicling red cancel button to cancel and stuff
#similarly, how do i get the start screen with instructions to trigger?
#should i bother with the companion cube element?


import random
import sys

import pygame
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, \
    K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL, K_RETURN, FULLSCREEN, K_q, K_r
pygame.init()

x_window_max = 800
y_window_max = 600

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


# class countdownTimer(pygame.sprite.Sprite):
#   def __init__(self):
#       t = f.render("Survive for " + str(time_limit) + " seconds!", False, (250,250,250))
#       # screen.blit(t, (0, y_window_max-50))
#       # self.add(everything)

#   def update(self, seconds):
#       screen.fill((0,0,0))
#       if seconds<(0.15*time_limit):
#           t = f.render("Survive for " + str(time_limit) + " seconds!", False, (250,250,250))
#       elif seconds>=(0.15*time_limit) and seconds<(0.6*time_limit):
#           t = f.render("Survive!", False, (250,250,250))
#       elif seconds>=(0.6*time_limit):
#           t = f.render("Almost there!", False, (250,250,250))
#       screen.blit(t, (0, y_window_max-50))

# class livesCounter(pygame.sprite.Sprite):
#   def __init__(self):
#       t = f.render(str(lives_limit) + " lives left", False, (250,250,250))

#   def update(self, health):
#       # screen.fill((0,0,0))
#       t = f.render(str(health) + " lives left", False, (250,250,250))
#       screen.blit(t, (0, y_window_max-80))

class endGame(pygame.sprite.Sprite):
    def __init__(self):
        endGame_t = f.render("     ", False, (250,250,250))

    def update(self, seconds, health):
        screen.fill((0,0,0))
        if seconds >= time_limit:
            endGame_t = f.render("You Won!", False, (34,139,34))
            print ("You Won!")
        if health <= 0:
            endGame_t = f.render("You Lost!", False, (178,34,34))
            print ("You Lost!")
        screen.blit(endGame_t, (x_window_max/2, y_window_max/2))

def end_game_func(seconds, health):
    screen.fill((0,0,0))
    if seconds >= time_limit:
        endGame_t = f.render("You Won!", False, (34,139,34))
        # screen.blit(endGame_t, (x_window_max/2, y_window_max/2))
        pygame.mixer.Sound("game_win_sound.wav").play()
        print ("Congratulations! You Won!")
    if health <= 0:
        endGame_t = f.render("You Lost!", False, (178,34,34))
        # screen.blit(endGame_t, (x_window_max/2, y_window_max/2))
        pygame.mixer.Sound("game_over_sound.wav").play()
        print ("On, No! You Lost!")
    gameExit = False
    while gameExit == False:
        screen.fill((0,0,0))
        screen.blit(endGame_t, (30, y_window_max/2))
        endOptions_t = f.render("Press any key to Quit.", False, (240,225,65))
        screen.blit(endOptions_t, (30, y_window_max-50))
        
        for event in pygame.event.get():
            if (event.type == KEYDOWN):
                gameExit = True
                break
                
        pygame.display.update()         
    pygame.quit()
    quit()
    # screen.blit(endGame_t, (x_window_max/2, y_window_max/2))
    
class lifeCountAndTimer(pygame.sprite.Sprite):
    def __init__(self):
        tC_t = f.render("Survive for " + str(time_limit) + " seconds!", False, (250,250,250))
        lC_t = f.render(str(lives_limit) + " lives left", False, (250,250,250))

    def update(self, seconds, health):
        screen.fill((0,0,0))
        if seconds<(0.15*time_limit):
            tC_t = f.render("Survive for " + str(time_limit) + " seconds!", False, (250,250,250))
        elif seconds>=(0.15*time_limit) and seconds<(0.6*time_limit):
            tC_t = f.render("Survive!", False, (250,250,250))
        elif seconds>=(0.6*time_limit):
            tC_t = f.render("Almost there!", False, (250,250,250))
        screen.blit(tC_t, (30, y_window_max-50))

        lC_t = f.render(str(health) + " lives left", False, (250,250,250))
        screen.blit(lC_t, (30, y_window_max-80))

class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, x_pos, groups):
        super(EnemySprite, self).__init__()
        self.image = pygame.image.load("enemy.bmp").convert_alpha()
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
        self.image = pygame.image.load("hero.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x_window_max/2, y_window_max/2 - 20)
        self.dx = self.dy = 0
        self.health = lives_limit

        self.groups = [groups]

        self.autopilot = False
        self.in_position = False
        self.velocity = 2

    def update(self):
        x, y = self.rect.center

        if not self.autopilot:
            # Handle movement
            self.rect.center = x + self.dx, y + self.dy

            # if self.health < 0:
            #   self.kill()
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

    
    enemies = pygame.sprite.Group()

    empty = pygame.Surface((x_window_max, y_window_max))
    clock = pygame.time.Clock()

    ship = CellSprite(everything)
    ship.add(everything)

    for i in range(10):
        pos = random.randint(0, x_window_max)
        EnemySprite(pos, [everything, enemies])

    # # Get some music
    # if pygame.mixer.get_init():
    #    pygame.mixer.music.load("DST-AngryMod.mp3")
    #    pygame.mixer.music.set_volume(0.8)
    #    pygame.mixer.music.play(-1)

    counterz = lifeCountAndTimer()
    eG = endGame()

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

        # Check for impact
        hit_ships = pygame.sprite.spritecollide(ship, enemies, True)
        for i in hit_ships:
            ship.health -= 1
            # mixer.Sound("game_hit_sound_1.wav").play()
            pygame.mixer.Sound("game_hit_sound_1.wav").play()

        if ship.health == 0:
            game_over = True

        if len(enemies) < 20 and not game_over:
            pos = random.randint(0, x_window_max)
            EnemySprite(pos, [everything, enemies])

        # Check for game over
        if seconds >= time_limit:
            game_over = True


        if game_over == True:
            end_game_func(seconds, ship.health)
            # pygame.time.delay(3000) #pauses game for 3 real-time seconds
            sys.exit()

        # Update sprites
        
        everything.clear(screen, empty)
        everything.update()
        everything.draw(screen)
        pygame.display.flip()
        counterz.update(seconds, ship.health)

# if __name__ == '__main__':
#   main()
main()