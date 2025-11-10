import pygame
import os

class State(pygame.sprite.Sprite):
    dir = os.path.dirname(os.path.dirname(__file__))

    def __init__(self, health_scale, health_x, health_y, man):
        super().__init__()
        self.health_scale = health_scale
        self.health_images = pygame.image.load(os.path.join(self.dir, 'resources', 'images', 'health.png')).convert_alpha()
        self.health_image = [pygame.transform.scale(self.health_images.subsurface(pygame.Rect(i * 46, 0, 46, 7)), self.health_scale) for i in range(7)]
        self.health_rect = self.health_images.get_rect(topleft=(health_x, health_y))
        self.current_health_image = self.health_image[0]
        self.man = man
        self.man.health = 100

    def State_update(self):
        if self.man.health >= 100:
            self.current_health_image = self.health_image[0] 
        elif self.man.health >= 90:
            self.current_health_image = self.health_image[1]
        elif self.man.health >= 70:
            self.current_health_image = self.health_image[2]
        elif self.man.health >= 50:
            self.current_health_image = self.health_image[3]
        elif self.man.health >= 30:
            self.current_health_image = self.health_image[4]
        elif self.man.health >= 10:
            self.current_health_image = self.health_image[5]
        else:
            self.current_health_image = self.health_image[6] 
            
    def Health(self):
        self.man.health -= 1
        self.State_update()
        
    def Magazine(self):
        pass

    def Stock(self):
        pass
    