import pygame
from game_resources import IMAGE_PLAY_BK

#游戏背景
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = IMAGE_PLAY_BK
        self.rect = self.image.get_rect()
        self.rect.left = -220

#11