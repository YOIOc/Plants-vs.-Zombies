import pygame
import random
import game_config
from game_config import WIDTH
from game_resources import IMAGE_PEABULLETHIT,\
                           WAV_BUTTLE_BREAK

#子弹父类
class _Bullet():
    def __init__(self, kind, atk, topleft):
        self.image = kind
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

        self.atk = atk               #子弹攻击力
        self.speed = 6               #子弹飞行速度
        self.hit_zombie_time = 0     #破碎的起始时间
        self.break_livedealy = 3.6   #破碎存在时间

        self.snow_bullet = False     #是否为功能子弹

    #碰撞僵尸
    def  hit_zombie(self, zombies):
        for zombie in zombies:
            if self.rect.colliderect(zombie.buttle_collide_rect):
                if self.snow_bullet:zombie.is_snow = True
                zombie.blood -= self.atk
                self.rect.center = zombie.rect.center
                self.image = IMAGE_PEABULLETHIT
                self.atk = 0
                self.speed = 0

    def update(self):
        if self.atk != 0:self.hit_zombie_time = game_config.FRAMECOUNT
        now = game_config.FRAMECOUNT
        #当子弹射出窗口、子弹破碎一段时间后kill
        if self.rect.left >= WIDTH or now - self.hit_zombie_time >= self.break_livedealy:
            random.choice(WAV_BUTTLE_BREAK).play()
            self.kill()

        self.rect.x += self.speed

#普通豌豆--子类
class PeaBullet(pygame.sprite.Sprite, _Bullet):
    def __init__(self, kind, atk, topleft):
        super().__init__()
        _Bullet.__init__(self, kind, atk, topleft)

    #静态方法(装饰器)--在不实例的情况下访问类中的参数
    @staticmethod
    def peafire_delay_long():
        return 81, 91
    
    @staticmethod
    def peafire_delay_short():
        return 15

    def update(self):
        _Bullet.update(self)

#寒冰豌豆--子类
class SnowBullet(pygame.sprite.Sprite, _Bullet):
    def __init__(self, kind, atk, topleft):
        super().__init__()
        _Bullet.__init__(self, kind, atk, topleft)

        self.snow_bullet = True

    def update(self):
        _Bullet.update(self)

#70