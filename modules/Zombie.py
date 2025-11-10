import pygame
import os
import time


class Zombie(pygame.sprite.Sprite):
    dir = os.path.dirname(os.path.dirname(__file__))

    def __init__(self, x, y, scale, screen_width, man):
        super().__init__()
        self.image = pygame.image.load(os.path.join(self.dir, 'resources', 'images', 'Zombie.png')).convert_alpha()
        self.scale = scale
        self.health_scale = (85,14)
        self.animation = [pygame.transform.scale(self.image.subsurface(pygame.Rect(i * 33, 0, 33, 35)), self.scale) for i in range(11)]
        self.death = [pygame.transform.scale(self.image.subsurface(pygame.Rect(i * 33, 0, 33, 35)), self.scale) for i in range(11,16)]
        self.health_images = pygame.image.load(os.path.join(self.dir, 'resources', 'images', 'Zombie_health.png')).convert_alpha()
        self.health_image = [pygame.transform.scale(self.health_images.subsurface(pygame.Rect(i * 46, 0, 46, 7)), self.health_scale) for i in range(7)]
        self.current_health_image = self.health_image[0]
        self.rect = self.animation[1].get_rect(topleft=(x, y))
        self.index = 0
        self.hit = 30
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
            if self.man.isdeath == True:
                self.current_action = "idle"
                self.current_speed = 0.2
            else:
                self.current_action = "attack"
                self.current_speed = 0.2

        else:
            if (keys[pygame.K_LEFT] or not self.rect.colliderect(self.man.rect)) and self.rect.x > 0:
                self.current_action = "walk"
                self.rect.x -= 2.3
                self.current_speed = 0.18
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
                if self.current_action == "idle":
                    self.index += 1
                    if self.index >= 4:
                        self.index = 0
                elif self.current_action == "attack" and not self.isdeath:
                    self.index += 1
                    if self.index >= 11:
                            self.index = 9
                else:
                    self.index += 1
                    if self.index >= 9:
                        self.index = 5

            self.last_score_update_time = current_time

    def health(self):
        if self.hit >= 30:
            self.current_health_image = self.health_image[0] 
        elif self.hit >= 25:
            self.current_health_image = self.health_image[1]
        elif self.hit >= 20:
            self.current_health_image = self.health_image[2]
        elif self.hit >= 15:
            self.current_health_image = self.health_image[3]
        elif self.hit >= 10:
            self.current_health_image = self.health_image[4]
        elif self.hit >= 5:
            self.current_health_image = self.health_image[5]
        else:
            self.current_health_image = self.health_image[6] 

    def get_image(self):    
        if not self.isdeath:
            return self.animation[self.index]
        else:
            return self.death[self.index]