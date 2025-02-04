import pygame
import os

class GameStart(pygame.sprite.Sprite):
    dir = os.path.dirname(os.path.dirname(__file__))

    def __init__(self, x, y, scale):
        super().__init__()
        self.scale = scale
        self.images = pygame.image.load(os.path.join(self.dir, 'resources', 'images', 'GameStart.png'))
        self.data = [pygame.transform.scale(self.images.subsurface(pygame.Rect(i * 640, 0, 640, 360)), self.scale) for i in range(5)]
        self.current_action = "original"
        self.image = self.data[0]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.change()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if (mouse_x  >= self.rect.width//3) and (mouse_x  <= self.rect.width//3*2): 
            if (mouse_y <= self.rect.height//2): 
                self.current_action = "START"
                if mouse_buttons[0]:
                    self.current_action = "START_TOUCH"
            elif (mouse_y >= self.rect.height//2): 
                self.current_action = "EXIT"
                if mouse_buttons[0]:
                    self.current_action = "EXIT_TOUCH"
        else:
            self.current_action = "original"

    def change(self):
        if self.current_action == "EXIT":
            self.image = self.data[1]
        elif self.current_action == "EXIT_TOUCH":
            self.image = self.data[2]
        elif self.current_action == "START":
            self.image = self.data[3]          
        elif self.current_action == "START_TOUCH":
            self.image = self.data[4]
        else:
            self.image = self.data[0]

    def get_image(self):
        return self.image