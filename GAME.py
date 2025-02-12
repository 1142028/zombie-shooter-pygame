import pygame
import sys
import time
import random
import os

from modules import Man
from modules import Zombie
from modules import Bullet
from modules import Machine
from modules import GameStart
from modules import State
#from modules import background

dir = os.path.dirname(os.path.dirname(__file__))

pygame.init()
SCREEN_W, SCREEN_H = SCREEN_SCALE = pygame.display.Info().current_w, pygame.display.Info().current_h
SCREEN = pygame.display.set_mode(SCREEN_SCALE)
pygame.display.set_caption("GAME")
clock = pygame.time.Clock()
last_score_update_time = time.time()

#GameStart
GameStart_X, GameStart_Y = (0, 0)
GameStart_SCALE = SCREEN_W, SCREEN_H
gamestart = GameStart(GameStart_X, GameStart_Y, GameStart_SCALE)

#Man
man_instance = False
MAN_X, MAN_Y = SCREEN_W // 10, SCREEN_H // 2
MAN_SCALE = bullet_SCALE = SCREEN_W // 7, SCREEN_H // 4
man = Man(MAN_X, MAN_Y, MAN_SCALE, SCREEN_W, SCREEN_H)
man_sprites = pygame.sprite.Group(man)

#Zombie
ZOMBIE_X, ZOMBIE_Y = SCREEN_W // 1.2, SCREEN_H // 2
ZOMBIE_SCALE= SCREEN_W // 7, SCREEN_H // 4
zombie = Zombie(ZOMBIE_X, ZOMBIE_Y, ZOMBIE_SCALE, SCREEN_W, man)
zombie_sprites = pygame.sprite.Group(zombie)
zombies = []

#Bullet
bullet_X, bullet_Y = man.rect.x, man.rect.y
bullet = Bullet(bullet_X, bullet_Y, bullet_SCALE, SCREEN_W, man_instance)
bullet_sprites = pygame.sprite.Group(bullet)
bullets = []

#Machine
machine_X, machine_Y = SCREEN_W // 5, SCREEN_H // 4
machine_SCALE = (50*5, 128*5)
machine = Machine(machine_X, machine_Y, machine_SCALE, man)
machine_sprites = pygame.sprite.Group(machine)

#background
background1 = pygame.image.load(os.path.join(dir,'2.5D橫向捲軸射擊', 'resources', 'images', 'background.png'))

#State
state = State.State(man)
state.man.health = 100

space_change = False
space_change_wait = 0

game_over = False
game_start = True

while game_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_start = False
        elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
            game_start = False
        elif gamestart.current_action == "START_TOUCH":
            game_start = False
            game_over = False
        elif gamestart.current_action == "EXIT_TOUCH":
            game_start = False

    SCREEN.blit(gamestart.get_image(), gamestart.rect.topleft)
    gamestart.update()

    pygame.display.flip()
    clock.tick(30)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            game_over = True    
        if man.rect.x <= -man.rect.width:
            space_change = True

    #renew
    man_sprites.update()
    zombie_sprites.update()
    machine_sprites.update()
    machine.update()

    #screen
    SCREEN.fill((80,90,130))
    SCREEN.blit(background1, (0,SCREEN_H*0.5))
    pygame.draw.rect(SCREEN, (36,32,49), [0, SCREEN_H * 0.96, SCREEN_W, SCREEN_H])
    if not space_change:     
        if man.rect.y >= zombie.rect.y:
            SCREEN.blit(machine.get_image(), machine.rect.topleft)
            SCREEN.blit(zombie.get_image(), zombie.rect.topleft)
            SCREEN.blit(man.get_image(), man.rect.topleft)
        elif man.rect.y <= zombie.rect.y:
            SCREEN.blit(machine.get_image(), machine.rect.topleft)
            SCREEN.blit(man.get_image(), man.rect.topleft)
            SCREEN.blit(zombie.get_image(), zombie.rect.topleft)
        if man.rect.y + man.rect.height+42 <= SCREEN_H*0.7:
            SCREEN.blit(man.get_image(), man.rect.topleft)
            SCREEN.blit(zombie.get_image(), zombie.rect.topleft)
            SCREEN.blit(machine.get_image(), machine.rect.topleft)        

    #bullet
    bullet_X, bullet_Y = man.rect.x, man.rect.y
    for bullet in bullets:
        bullet.update() 
        if bullet.rect.x >= SCREEN_W :
            bullets.remove(bullet)
        elif bullet.rect.x + bullet.rect.width >= zombie.rect.x + zombie.rect.width//2:
                if not zombie.isdeath:
                    zombie.rect.x +=2
                    zombie.hit += 1
                    bullets.remove(bullet)
                else:
                    SCREEN.blit(bullet.get_image(), bullet.rect.topleft)
        else:
            SCREEN.blit(bullet.get_image(), bullet.rect.topleft)
    if man.current_action == "shoot" and man.index == 10:
        man_instance = True
        new_bullet = Bullet(bullet_X, bullet_Y, bullet_SCALE, SCREEN_W, man_instance)
        bullets.append(new_bullet)

    #Man
    if not man.isdeath and not zombie.isdeath: 
            if man.rect.colliderect(zombie.rect):
                state.Health()
                if man.health <= 0 :
                    man.isdeath = True
                    man.index = 0

    #zombie
    if not zombie.isdeath:
        if zombie.hit >= 30:
            zombie.isdeath = True
            zombie.index = 0
    elif space_change==True:
        zombie.isdeath = False
        zombie.rect.x, zombie.rect.y = SCREEN_W // 1.2, SCREEN_H // 2
        zombie.hit = 0

    #machine
    if space_change:
        SCREEN.fill((20, 20, 20))
        machine.index = random.choice(range(6))
        space_change_wait += 1
        if space_change_wait >= 40:
            space_change_wait = 0
            man.rect.x, man.rect.y= SCREEN_W // 10, SCREEN_H // 2
            zombie.rect.x, zombie.rect.y = SCREEN_W // 1.2, SCREEN_H // 2
            space_change = False  

    #TEST
    for event in pygame.event.get():
        print(event) 

    pygame.display.update()
    clock.tick(144)

pygame.quit()
sys.exit()