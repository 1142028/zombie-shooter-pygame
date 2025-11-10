import pygame
import sys
import time
import os

from modules import Man
from modules import Zombie
from modules import Bullet
from modules import Machine
from modules import GameStart
from modules.State import State
from modules import background

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
MAN_X, MAN_Y = SCREEN_W // 12, SCREEN_H // 2
MAN_SCALE = SCREEN_W // 12, SCREEN_H // 7
man = Man(MAN_X, MAN_Y, MAN_SCALE, SCREEN_W, SCREEN_H)
man_sprites = pygame.sprite.Group(man)

#Zombie
ZOMBIE_X, ZOMBIE_Y = SCREEN_W , SCREEN_H // 2
ZOMBIE_SCALE= SCREEN_W // 12, SCREEN_H // 7
zombie = Zombie(ZOMBIE_X, ZOMBIE_Y, ZOMBIE_SCALE, SCREEN_W, man)
zombie_sprites = pygame.sprite.Group(zombie)
zombies = []

#Bullet
bullet_X, bullet_Y = man.rect.center
bullet_SCALE = (15*4, 1*4)
bullet = Bullet(bullet_X, bullet_Y, bullet_SCALE, SCREEN_W, man_instance)
bullet_sprites = pygame.sprite.Group(bullet)
bullets = []

#Machine
machine_X, machine_Y = SCREEN_W // 5, SCREEN_H // 2.15
machine_SCALE = (23*5, 34*5)
machine = Machine(machine_X, machine_Y, machine_SCALE, man)
machine_sprites = pygame.sprite.Group(machine)

#background
background1 = pygame.image.load(os.path.join(dir,'2.5D橫向捲軸射擊', 'resources', 'images', 'background.png'))
background_X, background_Y = (0,-340)
background_SCALE = (1920,1080)
background2 = background(background_X, background_Y, background_SCALE, SCREEN_W, man)

#State
health_scale = (85,14)
health_x, health_y = (man.rect.x,man.rect.y) 
zombie_health_x, zombie_health_y= (zombie.rect.x,zombie.rect.y) 
state = State(health_scale, health_x, health_y, man)
state.man.health = 100

#space_change
space_change = False
space_change_wait = 0

game = False
game_start = True

while game_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_start = False
        elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
            game_start = False
        elif gamestart.current_action == "START_TOUCH" or pygame.key.get_pressed()[pygame.K_SPACE]:
            game_start = False
            game = True
        elif gamestart.current_action == "EXIT_TOUCH":
            game_start = False

    SCREEN.blit(gamestart.get_image(), gamestart.rect.topleft)
    gamestart.update()

    pygame.display.flip()
    clock.tick(30)

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game= False
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            game = False   
        if man.rect.x <= -man.rect.width:
            space_change = True

    #renew
    man_sprites.update()
    zombie_sprites.update()
    machine_sprites.update()
    machine.update()

    #screen
    SCREEN.fill((150,150,200))
    SCREEN.blit(background1, (0,SCREEN_H*0.6))
    background2.update(SCREEN)
    pygame.draw.rect(SCREEN, (36,32,49), [0, SCREEN_H * 0.96, SCREEN_W, SCREEN_H])
    SCREEN.blit(state.current_health_image, (health_x, health_y))

    if man.rect.y >= zombie.rect.y:
        SCREEN.blit(zombie.current_health_image, (zombie_health_x, zombie_health_y))
        SCREEN.blit(zombie.get_image(), zombie.rect.topleft)
        SCREEN.blit(machine.get_image(), machine.rect.topleft)
        SCREEN.blit(man.get_image(), man.rect.topleft)
        SCREEN.blit(state.current_health_image, (health_x, health_y))
    elif man.rect.y <= zombie.rect.y:
        SCREEN.blit(machine.get_image(), machine.rect.topleft)
        SCREEN.blit(man.get_image(), man.rect.topleft)
        SCREEN.blit(state.current_health_image, (health_x, health_y))
        SCREEN.blit(zombie.current_health_image, (zombie_health_x, zombie_health_y))
        SCREEN.blit(zombie.get_image(), zombie.rect.topleft)
    if man.rect.y + man.rect.height <= SCREEN_H*0.62:
        SCREEN.blit(man.get_image(), man.rect.topleft)
        SCREEN.blit(state.current_health_image, (health_x, health_y))
        SCREEN.blit(zombie.current_health_image, (zombie_health_x, zombie_health_y))
        SCREEN.blit(zombie.get_image(), zombie.rect.topleft)
        SCREEN.blit(machine.get_image(), machine.rect.topleft)        

    #bullet
    bullet_X, bullet_Y = man.rect.x + 70, man.rect.y + 75
    Bullet.handle_bullets(SCREEN, bullets, zombie)
    if man.current_action == "shoot" and man.index == 11:
        man_instance = True
        new_bullet = Bullet(bullet_X, bullet_Y, bullet_SCALE, SCREEN_W, man_instance)
        bullets.append(new_bullet)

    #Man
    if not man.isdeath and not zombie.isdeath:
        if zombie.index == 10:
            state.Health()
            if man.health <= 0 :
                    man.isdeath = True
                    man.index = 0

    #State
    health_x, health_y = (man.rect.x + 15,man.rect.y - 15) 
    zombie_health_x, zombie_health_y= (zombie.rect.x + 50,zombie.rect.y - 15) 

    #Machine
    machine.business()
    
    #zombie
    if not zombie.isdeath:
        zombie.health()
        if zombie.hit <= 0:
            zombie.isdeath = True
            zombie.index = 0

    #space_change
    if space_change:
        SCREEN.fill((20, 20, 20))
        background2.reset()
        machine.change()
        space_change_wait += 1
        if space_change_wait >= 40:
            space_change_wait = 0
            man.rect.x= SCREEN_W // 12
            zombie.rect.x, zombie.rect.y = SCREEN_W // 1.2, SCREEN_H // 2
            zombie.hit = 30
            zombie.isdeath = False
            space_change = False  

    print(state.man.health)

    pygame.display.update()
    clock.tick(144)

pygame.quit()
sys.exit()