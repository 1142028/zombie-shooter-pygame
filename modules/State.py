import pygame
import os

class State(pygame.sprite.Sprite):
    dir = os.path.dirname(os.path.dirname(__file__))

    def __init__(self,man):
        super().__init__()
        self.man = man
        self.man.health = 20

    def Health(self):
        self.man.health -= 1
        if self.man.health <= 0 :
            self.man.isdeath=True
            
    def Magazine(self):
        pass
    def Stock(self):
        pass