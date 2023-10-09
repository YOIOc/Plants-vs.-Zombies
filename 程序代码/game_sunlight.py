import pygame
import random
import game_config
from game_resources import IMAGE_SUN,\
                           WAV_GET_SUNLIGHT
from game_ui import CardField

#阳光父类
class SunLight():
    def __init__(self):
        self.sun_num = 25

        self.image_index = 0
        self.image = IMAGE_SUN[self.image_index]
        self.rect = self.image.get_rect()

        #回收位置
        self.destination = (CardField.cardfield_pos()[0] + 40, CardField.cardfield_pos()[1] + 34)
        #回收距离
        self.distance_x = self.rect.centerx - self.destination[0]
        self.distance_y = self.rect.centery - self.destination[1]

        self.is_recycle = False      #是否回收
        self.is_down_size = False    #是否缩小尺寸

        self.start = game_config.FRAMECOUNT

    #回收阳光
    def recycle_sun(self):
        self.distance_x = self.rect.centerx - self.destination[0]
        self.distance_y = self.rect.centery - self.destination[1]

        if not(self.is_recycle):return

        #回收速度
        speed_x = self.distance_x / 10
        speed_y = self.distance_y / 10
        self.rect.x -= speed_x
        self.rect.y -= speed_y

    #删除阳光
    def kill_sun(self,sun_livetime):
        now = game_config.FRAMECOUNT
        #阳光未被回收
        if not(self.is_recycle) and now - self.start > sun_livetime:
            self.kill()
        #阳光被回收
        if self.is_recycle and abs(self.distance_x) < 10 and abs(self.distance_y) < 10:
            self.kill()
            game_config.GAME_SUNNUMS += self.sun_num

    #是否回收阳光、回收的阳光是否进入缩小区域
    def handle_event(self, events, is_use_mouse):
        for e in events:
            #回收阳光
            if e.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(e.pos) and not is_use_mouse:
                WAV_GET_SUNLIGHT.play()
                self.is_recycle = True
        #进入缩小区域
        if self.is_recycle and abs(self.distance_x) < 24 and abs(self.distance_y) < 24:
            self.is_down_size = True

    #检查鼠标是否被使用
    def is_use_mouse(self):
        return self.is_recycle

    def update(self):
        self.recycle_sun()
        self.image_index = (self.image_index + 1) % len(IMAGE_SUN)
        if not self.is_down_size:
            self.image = IMAGE_SUN[self.image_index]
        else: 
            self.image = pygame.transform.scale(IMAGE_SUN[self.image_index], (abs(self.rect.width - 8), abs(self.rect.height - 8)))
        self.rect = self.image.get_rect(center=self.rect.center)

#由植物产生的阳光--子类
class SunLight_Plant(pygame.sprite.Sprite, SunLight):
    def __init__(self, pos):
        super().__init__()
        SunLight.__init__(self)

        self.top = pos
        self.random_pos()

        self.livetime_plant = 180    #存在时间
    
    #随机产生位置
    def random_pos(self):
        if random.choice([True, False]):
            self.rect.topright = self.top
        else:
            self.rect.topleft = self.top

    #产生延迟
    @staticmethod
    def delay_plant():
        return (180, 750), (1410, 1500)

    def update(self):
        SunLight.update(self)
        self.kill_sun(self.livetime_plant)

#由天空飘落的阳光--子类
class SunLight_Sky(pygame.sprite.Sprite, SunLight):
    def __init__(self):
        super().__init__()
        SunLight.__init__(self)

        self.rect.center = random.randint(124, 761), -40

        self.fall_speed = 1          #飘落速度
        self.livetime_sky = 750      #存在时间

    #飘落延迟
    @staticmethod
    def delay_sky():
        return 600
    
    def update(self):
        SunLight.update(self)
        self.kill_sun(self.livetime_sky)

        if self.rect.bottom <= 570 and not(self.is_recycle):
            self.rect.y += self.fall_speed

#121