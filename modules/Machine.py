import pygame
import os

class Machine(pygame.sprite.Sprite):
    dir = os.path.dirname(os.path.dirname(__file__))

    def __init__(self, x, y, scale, man):
        super().__init__()
        self.scale = scale
        self.images = pygame.image.load(os.path.join(self.dir, 'resources', 'images', 'Machine.png'))
        self.image = [pygame.transform.scale(self.images.subsurface(pygame.Rect(i * 50, 0, 50, 128)), self.scale) for i in range(6)]
        self.rect = self.images.get_rect(topleft=(x, y))
        self.man = man
        self.index = 0
    def update(self):
        keys = pygame.key.get_pressed()
        if self.rect.colliderect(self.man.rect) and keys[pygame.K_r]:
                self.business()

    def business(self):
        #if self.index == 0:
        self.man.current_speed += 1
        
    def get_image(self):
        if self.index >= len(self.image):
            self.index = 0
        return self.image[self.index]    