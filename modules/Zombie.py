import pygame
import os
import time


class Zombie(pygame.sprite.Sprite):
    dir = os.path.dirname(os.path.dirname(__file__))

    def __init__(self, x, y, scale, screen_width, man):
        super().__init__()
        self.image = pygame.image.load(os.path.join(self.dir, 'resources', 'images', 'Zombie.png'))
        self.scale = scale
        self.animation = [pygame.transform.scale(self.image.subsurface(pygame.Rect(i * 64, 0, 64, 64)), self.scale) for i in range(9)]
        self.death = [pygame.transform.scale(self.image.subsurface(pygame.Rect(i * 64, 0, 64, 64)), self.scale) for i in range(9,14)]
        self.rect = self.animation[1].get_rect(topleft=(x, y))
        self.index = 0
        self.hit = 0
        self.isdeath=False
        self.man = man
        self.current_action = "idle"
        self.current_speed = 0.2
        self.screen_width = screen_width
        self.last_score_update_time = time.time()

    def update(self):
        self.animate()
        keys = pygame.key.get_pressed()
        if self.isdeath:
            self.current_action = "death"
            self.current_speed = 0.15
        elif self.rect.colliderect(self.man.rect):
                self.current_action = "idle"
                self.current_speed = 0.15
        else:
            if (keys[pygame.K_LEFT] or not self.rect.colliderect(self.man.rect)) and self.rect.x > 0:
                self.current_action = "walk"
                self.rect.x -= 3.3
                self.current_speed = 0.2
            if (keys[pygame.K_UP] or not self.man.rect.y >= self.rect.y) and self.rect.x <= self.screen_width:
                self.current_action = "walk"
                self.current_speed = 0.14
                self.rect.y -= 0.6
            if (keys[pygame.K_DOWN] or not self.man.rect.y <= self.rect.y) and self.rect.x <= self.screen_width:
                self.current_action = "walk"
                self.current_speed = 0.14
                self.rect.y += 0.6
            
        
    def animate(self):
        current_time = time.time()
        if current_time - self.last_score_update_time >= self.current_speed:
            if self.isdeath:
                    self.index += 1
                    if self.index >= len(self.death):
                        self.index = len(self.death) - 1
                        self.isdeath = True
            else:
                if self.current_action == "walk":
                    self.index += 1
                    if self.index >= 4:
                        self.index = 0
                else:
                    self.index += 1
                    if self.index >= 9:
                        self.index = 4

            self.last_score_update_time = current_time

    def get_image(self):
        if not self.isdeath:
            return self.animation[self.index]
        else:
            return self.death[self.index]