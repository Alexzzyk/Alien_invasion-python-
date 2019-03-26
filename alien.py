import pygame
from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.screen_rect = screen.get_rect()
        self.speed_factor = ai_settings.alien_speed_factor
    def check_edges(self):
        if self.rect.right > self.screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        self.x += self.speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x