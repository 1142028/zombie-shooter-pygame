import pygame
import os

class background(pygame.sprite.Sprite):
    dir = os.path.dirname(os.path.dirname(__file__))

    def __init__(self, x, y, scale, screen_width, man):
        super().__init__()
        self.scale = scale
        self.man = man
        self.screen_width = screen_width
        self.images = pygame.image.load(os.path.join(self.dir, 'resources', 'images', 'background2.png'))
        self.data = [pygame.transform.scale(self.images.subsurface(pygame.Rect(i * 512, 0, 512, 288)), self.scale) for i in range(3)]
        self.current_action = 0
        self.image = self.data[self.current_action]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        if self.man.rect.x >= 1915:
            self.current_action = (self.current_action + 1) % len(self.data)
            self.image = self.data[self.current_action]

    def get_image(self):
        return self.image