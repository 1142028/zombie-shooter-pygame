import pygame
import os

class background(pygame.sprite.Sprite):
    dir = os.path.dirname(os.path.dirname(__file__))

    def __init__(self, x, y, scale, screen_width, man):
        super().__init__()
        self.scale = scale
        self.man = man
        self.screen_width = screen_width
        self.last_man_x = man.rect.x  

        self.images = pygame.image.load(os.path.join(self.dir, 'resources', 'images', 'background2.png')).convert_alpha()
        self.data = [pygame.transform.scale(self.images.subsurface(pygame.Rect(i * 512, 0, 512, 288)),self.scale) for i in range(4)] 

        self.rect_front = self.data[3].get_rect(topleft=(x, y))
        self.rect_front2 = self.data[3].get_rect(topleft=(x + screen_width, y))
        self.rect_middle = self.data[2].get_rect(topleft=(x, y))
        self.rect_middle2 = self.data[2].get_rect(topleft=(x + screen_width, y))
        self.rect_bottom = self.data[1].get_rect(topleft=(x, y))
        self.rect_bottom2 = self.data[1].get_rect(topleft=(x + screen_width, y))

        self.static_pos = float(x)
        self.static2_pos = float(x + screen_width)
        self.middle_move = float(x)
        self.middle2_move = float(x + screen_width)
        self.bottom_move = float(x)
        self.bottom2_move = float(x + screen_width)

    def update(self, SCREEN):
        delta_x = self.man.rect.x - self.last_man_x

        self.middle_move -= delta_x * 0.12
        self.middle2_move -= delta_x * 0.12
        self.bottom_move -= delta_x * 0.2
        self.bottom2_move -= delta_x * 0.2 

        self.rect_middle.x = int(self.middle_move)
        self.rect_middle2.x = int(self.middle2_move)
        self.rect_bottom.x = int(self.bottom_move)
        self.rect_bottom2.x = int(self.bottom2_move)  

        self.rect_front.x = int(self.static_pos)
        self.rect_front2.x = int(self.static2_pos)

        if self.rect_middle.right <= 0:
            self.middle_move += self.screen_width * 2 
            self.rect_middle.x = int(self.middle_move)
        if self.rect_middle2.right <= 0:
            self.middle2_move += self.screen_width * 2
            self.rect_middle2.x = int(self.middle2_move)

        if self.rect_bottom.right <= 0:
            self.bottom_move += self.screen_width * 2 
            self.rect_bottom.x = int(self.bottom_move)
        if self.rect_bottom2.right <= 0:
            self.bottom2_move += self.screen_width * 2  
            self.rect_bottom2.x = int(self.bottom2_move)

        if self.rect_front.right <= 0:
            self.static_pos += self.screen_width * 2
            self.rect_front.x = int(self.static_pos)
        if self.rect_front2.right <= 0:
            self.static2_pos += self.screen_width * 2
            self.rect_front2.x = int(self.static2_pos)

        SCREEN.blit(self.data[1], self.rect_bottom.topleft)  
        SCREEN.blit(self.data[1], self.rect_bottom2.topleft)    
        SCREEN.blit(self.data[2], self.rect_middle.topleft)   
        SCREEN.blit(self.data[2], self.rect_middle2.topleft)    
        SCREEN.blit(self.data[3], self.rect_front.topleft)   
        SCREEN.blit(self.data[3], self.rect_front2.topleft)   

        self.last_man_x = self.man.rect.x

    def reset(self):
        self.static_pos = 0.0
        self.static2_pos = float(self.screen_width)
        self.middle_move = 0.0
        self.middle2_move = float(self.screen_width)
        self.bottom_move = 0.0
        self.bottom2_move = float(self.screen_width)
