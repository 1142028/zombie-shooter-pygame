import pygame
import os
import time

class Man(pygame.sprite.Sprite):
    dir = os.path.dirname(os.path.dirname(__file__))

    def __init__(self, x, y, scale, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load(os.path.join(self.dir, 'resources', 'images', 'Man.png')).convert_alpha()
        self.scale = scale
        self.animation = [pygame.transform.scale(self.image.subsurface(pygame.Rect(i * 35, 0, 35, 36)), self.scale) for i in range(13)]
        self.death = [pygame.transform.scale(self.image.subsurface(pygame.Rect(i * 35, 0, 35, 36)), self.scale) for i in range(14,20)]
        self.rect = self.animation[0].get_rect(topleft=(x, y))
        self.rect = self.rect.inflate(100-self.rect.width,0)
        self.isdeath=False
        self.index = 0
        self.current_action = "idle"
        self.current_speed = 0.15
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.last_score_update_time = time.time()

    def update(self):
        self.animate()
        keys = pygame.key.get_pressed()

        if self.isdeath:
            self.current_action = "death"
            self.current_speed = 0.3
        else:
            if keys[pygame.K_a] and self.rect.x > 0:
                self.current_action = "walk"
                self.rect.x -= 2
                self.current_speed = 0.2
            elif keys[pygame.K_e]:
                self.current_action = "shoot"
                self.current_speed = 0.09
            elif keys[pygame.K_d] and self.rect.x < self.screen_width and not (self.rect.x <= -self.rect.width):
                self.current_action = "walk"
                self.rect.x += 4
                self.current_speed = 0.13
            elif keys[pygame.K_w] and self.rect.y + self.rect.height  >= self.screen_height *0.61:
                self.current_action = "walk"
                self.rect.y -= 3
                self.current_speed = 0.13
            elif keys[pygame.K_s] and self.rect.y + self.rect.height  <= self.screen_height *0.83:
                self.current_action = "walk"
                self.rect.y += 3
                self.current_speed = 0.13
            else:
                self.current_action = "idle"
                self.current_speed = 0.15
            if self.rect.x >= self.screen_width:
                self.rect.x = -self.screen_width

        

    def animate(self):
            current_time = time.time()
            if current_time - self.last_score_update_time >= self.current_speed:
                if self.isdeath:
                    self.index += 1
                    if self.index >= len(self.death):
                        self.index = len(self.death) - 1
                        self.isdeath = True
                else:
                    if self.current_action == "walk" and not self.isdeath:
                        self.index += 1
                        if self.index >= 4:
                            self.index = 0
                    elif self.current_action == "shoot" and not self.isdeath:
                        self.index += 1
                        if self.index >= 13:
                            self.index = 9
                    else:
                        self.index += 1
                        if self.index >= 11:
                            self.index = 5
                            
                self.last_score_update_time = current_time

    def get_image(self):
        if not self.isdeath:
            return self.animation[self.index] if 0 <= self.index < len(self.animation) else self.animation[0]
        else:
            return self.death[self.index]
        