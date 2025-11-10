import pygame
import os
import time

class Bullet(pygame.sprite.Sprite):
    dir = os.path.dirname(os.path.dirname(__file__))
    MAX_INDEX = 9
    MOVE_SPEED = 50

    def __init__(self, x, y, scale, screen_width, man_instance):
        super().__init__()
        self.scale = scale
        self.images = pygame.transform.scale(pygame.image.load(os.path.join(self.dir, 'resources', 'images', 'bullet.png')).convert_alpha(),self.scale)
        self.rect = self.images.get_rect(topleft=(x, y))
        self.current_action = False
        self.current_speed = 0.1
        self.screen_width = screen_width
        self.man_instance = man_instance  
        self.last_update_time = time.time()

    def update(self):
        self.move()
        self.animate()

    def move(self):
        if self.man_instance:
            self.rect.x += self.MOVE_SPEED

    def animate(self):
        current_time = time.time()
        if current_time - self.last_update_time >= self.current_speed:
            self.last_update_time = current_time

    def get_image(self):
        return self.images

    def handle_bullets(screen, bullets, zombie):
        for bullet in bullets[:]:
            bullet.update()
            if bullet.rect.colliderect(zombie.rect) and bullet.rect.x + bullet.rect.width >= zombie.rect.x + zombie.rect.width // 1.5:
                if not zombie.isdeath:
                    zombie.rect.x += 0.2 
                    zombie.hit -= 1 
                    bullets.remove(bullet)  
                else:
                    screen.blit(bullet.get_image(), bullet.rect.topleft)
            else:
                screen.blit(bullet.get_image(), bullet.rect.topleft)