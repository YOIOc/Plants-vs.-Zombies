import pygame
import random
import game_config
from game_config import GAME_ZOMBIE_BLOOD, GAME_ZOMBIE_ATK, GAME_ZOMBIE_SPEED
from game_resources import IMAGE_ZOMBIE, IMAGE_FLAGZOMBIE, IMAGE_CONEZOMBIE, IMAGE_BUCKETZOMBIE, IMAGE_LOSEHEAD, IMAGE_ZOMBIEDIE, IMAGE_ZOMBIEBACK, IMAGE_ZOMBIEBOOMDIE,\
                           WAV_LAWNMOWER, WAV_EAT, WAV_LOSE_HEAD, WAV_SCREAM

#僵尸父类
class _Zombie():

    #僵尸头颅动画
    class _ZombieHead(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            WAV_LOSE_HEAD.play()

            self.image_index_head = 0
            self.image = IMAGE_LOSEHEAD[self.image_index_head]
            self.rect = self.image.get_rect()
            self.rect.topleft = x, y

        def update(self):
            self.image_index_head = (self.image_index_head + 1) % len(IMAGE_LOSEHEAD)
            self.image = IMAGE_LOSEHEAD[self.image_index_head]
            if self.image_index_head + 1 == len(IMAGE_LOSEHEAD):self.kill()     #当头颅掉落图片全部索引完后kill

    def __init__(self, pos, image, kind):

        self.is_eat = 0       #0为正常状态 / 1为啃食状态
        self.is_losehead = 0  #0为正常状态 / 1为濒死状态
        self.is_die = 0       #0为正常状态 / 1为死亡状态

        self.image_index_live = 0    #活着时4种图片的索引
        self.image_index_die = -1    #死亡时的图片索引
        self.image_index_boom = 0    #被炸死时的图片索引
        self.image_index_back = 0    #被小车碾压的图片索引
        self.zombie_image = image
        self.image = self.zombie_image[self.is_eat][self.is_losehead][self.image_index_live]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos

        #僵尸不同的碰撞区域
        self.plant_collide_rect = pygame.Rect(self.rect.left+90, self.rect.top+90, 45, 30)
        self.buttle_collide_rect = pygame.Rect(self.rect.left+75, self.rect.top+21, 45, 120)
        self.lawncleaner_collide_rect = pygame.Rect(self.rect.left+75, self.rect.top+119, 53, 25)

        #僵尸的基础属性
        self.kind = kind
        self.blood = GAME_ZOMBIE_BLOOD[self.kind]
        self.atk = GAME_ZOMBIE_ATK[self.kind]
        self.speed = GAME_ZOMBIE_SPEED[self.kind]

        #僵尸的状态参数
        self.is_boom = False              #是否被炸
        self.is_snow = False              #是否减速
        self.is_hit_lawncleaner = False   #是否碰撞小车

        #不同状态下的fps
        self.move_fps = 16
        self.eat_fps = 8
        self.die_fps = 4

        self.eat_play = False

    #自定义碰撞检测方式
    def collide(self, sprite1, sprite2):
        if sprite2.rect.collidepoint((sprite1.rect.left + 90, sprite1.rect.top + 90)) or sprite2.rect.collidepoint((sprite1.rect.left + 90, sprite1.rect.top + 120)):return True
        return False
    
    #啃食植物
    def eat_plant(self, plants):
            plant = pygame.sprite.spritecollideany(self, plants, collided=self.collide)
            #满足条件--啃食
            if plant:
                #在不播放啃食音效的时候再播放
                voice = pygame.mixer.Channel(5)
                if not voice.get_busy():
                    sound = random.choice(WAV_EAT)
                    voice.play(sound)

                self.is_eat = 1
                self.speed = 0
                plant.blood -= self.atk
            #不满足条件--行走
            else:
                self.is_eat = 0
                self.speed = GAME_ZOMBIE_SPEED[self.kind]

    #碰撞小车
    def hit_lawncleaner(self, lawncleaners):
        for lawncleaner in lawncleaners:
            if self.lawncleaner_collide_rect.colliderect(lawncleaner.rect):
                if lawncleaner.speed == 0:
                    WAV_LAWNMOWER.play(-1)
                    WAV_LAWNMOWER.fadeout(2500)
                lawncleaner.speed = 5
                self.is_hit_lawncleaner = True

    #不同僵尸状态下采用不同fps
    def refresh(self):
        if self.is_eat == 0 and self.is_die == 0:return game_config.FRAMECOUNT % self.move_fps == 0 if not self.is_snow else game_config.FRAMECOUNT % (self.move_fps*2) == 0
        if self.is_eat != 0 and self.is_die == 0:return game_config.FRAMECOUNT % self.eat_fps == 0 if not self.is_snow else game_config.FRAMECOUNT % (self.eat_fps*2) == 0
        if self.is_die == 1:return game_config.FRAMECOUNT % self.die_fps == 0 

    def kill_zombie(self):
        self.kill()

    def update(self):
        #当血量低于0时
        if (not self.is_boom) and self.blood <= 0:
            self.is_die = 1
            self.image_index_die = (self.image_index_die + 1) % len(IMAGE_ZOMBIEDIE)
            self.image = IMAGE_ZOMBIEDIE[self.image_index_die]
            if self.image_index_die + 1 == len(IMAGE_ZOMBIEDIE):self.kill_zombie()
            return
        #当血量等于90时
        if self.blood == 90:
            if self.is_losehead == 0:
                _Zombie._ZombieHead(self.rect.left + 57, self.rect.top).add(self.alls_sprites)
            self.is_losehead = 1
        #当被炸时
        if self.is_boom:
            self.is_die = 1
            self.image_index_boom = (self.image_index_boom + 1) % len(IMAGE_ZOMBIEBOOMDIE)
            self.image = IMAGE_ZOMBIEBOOMDIE[self.image_index_boom]
            if self.image_index_boom + 1 == len(IMAGE_ZOMBIEBOOMDIE):self.kill_zombie()
            return
        #当撞击小车时
        if self.is_hit_lawncleaner:
            self.is_die = 1
            self.image_index_back = (self.image_index_back + 1) % len(IMAGE_ZOMBIEBACK)
            self.image = IMAGE_ZOMBIEBACK[self.image_index_back]
            if self.image_index_back + 1 == len(IMAGE_ZOMBIEBACK):self.kill_zombie()
            return
        
        self.atk = GAME_ZOMBIE_ATK[self.kind] // 2 if self.is_snow else GAME_ZOMBIE_ATK[self.kind]                     #更新僵尸的攻击力
        self.speed = GAME_ZOMBIE_SPEED[self.kind] if self.is_eat != 1 else 0                                           #更新僵尸的速度
        self.rect.x -= self.speed
        self.buttle_collide_rect = pygame.Rect(self.rect.left+80, self.rect.top+21, 45, 120)
        self.lawncleaner_collide_rect = pygame.Rect(self.rect.left+75, self.rect.top+119, 53, 25)
        self.image_index_live = (self.image_index_live + 1) % len(self.zombie_image[self.is_eat][self.is_losehead])
        self.image = self.zombie_image[self.is_eat][self.is_losehead][self.image_index_live]

#普通僵尸--子类
class Zombie(pygame.sprite.Sprite, _Zombie):
    def __init__(self, alls, pos):
        super().__init__()
        _Zombie.__init__(self, pos, IMAGE_ZOMBIE, "Zombie")

        self.alls_sprites = alls

    def update(self):
        if not self.refresh(): return
        _Zombie.update(self)

#旗帜僵尸--子类
class FlagZombie(pygame.sprite.Sprite, _Zombie):
    def __init__(self, alls, pos):
        super().__init__()
        _Zombie.__init__(self, pos, IMAGE_FLAGZOMBIE, "FlagZombie")

        self.alls_sprites = alls

    def update(self):
        if not self.refresh(): return
        _Zombie.update(self)

#路障僵尸--子类
class ConeheadZombie(pygame.sprite.Sprite, _Zombie):
    def __init__(self, alls, pos):
        super().__init__()
        _Zombie.__init__(self, pos, IMAGE_CONEZOMBIE, "ConeheadZombie")

        self.alls_sprites = alls

    def update(self):
        if not self.refresh(): return
        _Zombie.update(self)

#铁通僵尸--子类
class BucketheadZombie(pygame.sprite.Sprite, _Zombie):
    def __init__(self, alls, pos):
        super().__init__()
        _Zombie.__init__(self, pos, IMAGE_BUCKETZOMBIE, "BucketheadZombie")

        self.alls_sprites = alls

    def update(self):
        if not self.refresh(): return
        _Zombie.update(self)

#190