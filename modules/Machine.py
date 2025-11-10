import pygame
import os
import random

class Machine(pygame.sprite.Sprite):
    dir = os.path.dirname(os.path.dirname(__file__))

    def __init__(self, x, y, scale, man):
        super().__init__()
        self.scale = scale
        self.images = pygame.image.load(os.path.join(self.dir, 'resources', 'images', 'Machine.png')).convert_alpha()
        self.image = [pygame.transform.scale(self.images.subsurface(pygame.Rect(i * 23, 0, 23, 34)), self.scale) for i in range(6)]
        self.rect = self.images.get_rect(topleft=(x, y))
        self.man = man
        self.index = 0

    def update(self):
        pass

    def business(self):
        if self.index == 0:
            pass
        if self.index == 1:
            pass
        if self.index == 2:
            pass
        if self.index == 3:
            pass
        if self.index == 4:
            pass
        if self.index == 5:
            pass

    def change(self):
        self.index = random.choice(range(6))
         
    def get_image(self):
        if self.index >= len(self.image):
            self.index = 0
        return self.image[self.index]    