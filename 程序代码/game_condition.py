import pygame
import random
import game_config
from game_config import WIDTH, HEIGHT, EVENT_GAME_OVER
from game_resources import IMAGE_WAVE, IMAGE_LOSEGAME, IMAGE_ZOMBIENOTE, IMAGE_VICTORY_GAME,\
                           WAV_READYGO, WAV_AWOOGA, WAV_ZOMBIE_GROWL, WAVE_HUGEWAVE, WAVE_FINALWAVE

#波次父类
class _Wave():
    def __init__(self, size):
        self.screen_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center = self.screen_rect.center)
        self.img = None
        self.size = size

        #相关参数
        self.alpha = 255
        self.alpha_speed = 0
        self.factor = 1.0
        self.factor_speed = 0
        self.bron_time = game_config.FRAMECOUNT

    def update(self):
        self.alpha -= self.alpha_speed
        self.image.set_alpha(self.alpha)
        self.factor += self.factor_speed
        self.image = pygame.transform.scale(self.image, (int(self.size[0] * self.factor), int(self.size[1] * self.factor)))
        self.rect = self.image.get_rect(center = self.screen_rect.center)
        img = pygame.transform.scale(self.img, (int(self.size[0] * self.factor), int(self.size[1] * self.factor)))
        rect = img.get_rect()
        rect.left = (self.rect.width-rect.width)//2
        rect.top = (self.rect.height-rect.height)//2
        self.image.blit(img, rect)

#开始一波 -- 波次子类
class Start_Wave(pygame.sprite.Sprite, _Wave):
    def __init__(self):
        super().__init__()
        _Wave.__init__(self, (300, 133))
        sound = WAV_READYGO.play()
        sound.queue(WAV_AWOOGA)
        sound.queue(random.choice(WAV_ZOMBIE_GROWL))
        
        self.image_index = 0
        self.img = IMAGE_WAVE[0][self.image_index]
        
        self.alpha_speed = 4
        self.factor_speed = 0.002
        self.being_daley = 42         #显示时间

    def update(self):
        now = game_config.FRAMECOUNT
        if now - self.bron_time >= self.being_daley:
            if self.image_index + 1 == len(IMAGE_WAVE[0]):self.kill()

            #绘制新图片
            self.image_index = (self.image_index + 1) % len(IMAGE_WAVE[0])
            self.image = pygame.Surface((300, 133), pygame.SRCALPHA)
            self.img = IMAGE_WAVE[0][self.image_index]
            #重新设置参数
            self.alpha = 255
            self.bron_time = now
            self.factor = 1.0
        _Wave.update(self)

#中间波 -- 波次子类
class Middle_Wave(pygame.sprite.Sprite, _Wave):
    def __init__(self):
        super().__init__()
        _Wave.__init__(self, (492, 80))
        WAVE_HUGEWAVE.play()

        self.img = IMAGE_WAVE[1]

        self.alpha_speed = 0.5
        self.factor_speed = 0.001
        self.being_daley = 240

    def update(self):
        now = game_config.FRAMECOUNT
        if now - self.bron_time >= self.being_daley:
            self.kill()
        _Wave.update(self)

#最后一波 -- 波次子类
class End_Wave(pygame.sprite.Sprite, _Wave):
    def __init__(self):
        super().__init__()
        _Wave.__init__(self, (341, 80))
        WAVE_FINALWAVE.play()

        self.img = IMAGE_WAVE[2]

        self.alpha_speed = 0.5
        self.factor_speed = 0.001
        self.being_daley = 240

    def update(self):
        now = game_config.FRAMECOUNT
        if now - self.bron_time >= self.being_daley:
            self.kill()
        _Wave.update(self)

#僵尸吃掉了你的脑子！
class Game_Defeated(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.screen_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)

        self.image = pygame.Surface((564, 468))
        self.size = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect(center = self.screen_rect.center)

        self.factor = 0.0
        self.is_kille = False
    
    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def update(self):
        if self.is_kille:
            self.kill()                                    
            return
        
        if self.factor < 1:
            self.factor += 0.01
        self.image = pygame.transform.scale(IMAGE_LOSEGAME, (int(self.size[0] * self.factor), int(self.size[1] * self.factor)))
        self.rect = self.image.get_rect(center = self.screen_rect.center)

#你胜利了
class Game_Victory(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.screen_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        
        self.image = pygame.Surface((654, 427))
        self.size_bk = self.image.get_size()
        self.rect = self.image.get_rect(center = self.screen_rect.center)
        
        self.image_write = IMAGE_VICTORY_GAME
        self.size_write = self.image_write.get_size()
        self.rect_write = self.image_write.get_rect()

        self.factor = 0.0
        self.is_kille = False

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def update(self):
        if self.is_kille:
            self.kill()
            e = pygame.event.Event(EVENT_GAME_OVER, {"state":False})
            pygame.event.post(e)                                      
            return
        
        if self.factor < 1:
            self.factor += 0.01
        self.image = pygame.transform.scale(IMAGE_ZOMBIENOTE, (int(self.size_bk[0] * self.factor), int(self.size_bk[1] * self.factor)))
        self.rect = self.image.get_rect(center = self.screen_rect.center)
        self.image_write = pygame.transform.scale(IMAGE_VICTORY_GAME, (int(self.size_write[0] * self.factor), int(self.size_write[1] * self.factor)))
        self.rect_write = self.image_write.get_rect()
        self.rect_write.left = (self.rect.width-self.rect_write.width)//2
        self.rect_write.top = (self.rect.height-self.rect_write.height)//2
        self.image.blit(self.image_write, self.rect_write)

#166