import pygame
import sys
import os
import time

pygame.init()

dir = os.path.dirname(__file__)
man_image = pygame.image.load(os.path.join(dir, 'resources', 'images', 'Man.png'))
Man_image_w, Man_image_h = man_image.get_size()

SCREEN_W,SCREEN_H = SCREEN_SCALE=pygame.display.Info().current_w,pygame.display.Info().current_w
screen = pygame.display.set_mode(SCREEN_SCALE)
pygame.display.set_caption("GAME_TEST")
clock = pygame.time.Clock()
last_score_update_time = time.time()

MAN_X = SCREEN_W//10
MAN_Y = SCREEN_H//2
MAN_W,MAN_H = MAN_SCALE = SCREEN_W//7,SCREEN_H//7
man =[]
for i in range(15):
    man_rect = pygame.Rect(i * 64, 0, 64, 64)
    man.append(pygame.transform.scale(man_image.subsurface(man_rect),MAN_SCALE))

current_speed=0.15
index = 0
stop = False
game_over = False
current_action = "idle" 

while not game_over:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if keys[pygame.K_ESCAPE]:
            game_over = True
        if stop == True:
            game_over = True



    screen.fill((170,170,150))
    pygame.draw.rect(screen,(110,120,110),[0,SCREEN_H*0.6,SCREEN_W,SCREEN_H])

    current_time = time.time()
    if stop == True:
        current_time = 0
    if current_time - last_score_update_time >= current_speed:
        if current_action == "walk":
            index += 1
            if index >= 4:
                index = 0
        elif current_action == "shoot":
            index +=1
            if index >=12:
                index = 9  
        else:
            index += 1
            if index >= 9:
                index = 4

        last_score_update_time = current_time

    screen.blit(man[index], (MAN_X, MAN_Y))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and MAN_X > 0:
        current_action = "walk"
        MAN_X -= 2
        current_speed=0.2
    elif keys[pygame.K_w]:
            current_action = "shoot"
            current_speed=0.05
    elif keys[pygame.K_d] and MAN_X < SCREEN_W:
        current_action = "walk"
        current_speed=0.13
        MAN_X += 3.5
    else:
        current_action = "idle"
        current_speed=0.15
    if MAN_X >= SCREEN_W:
        MAN_X =- MAN_W
        




    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()