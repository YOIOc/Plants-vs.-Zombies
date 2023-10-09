import pygame
import random
import game_config
from game_config import GAME_PLANT_BLOOD, GAME_PLANT_ATK, WIDTH
from game_resources import IMAGE_SUNFLOWER, IMAGE_PEASHOOTER, IMAGE_SNOWPEASHOOTER, IMAGE_WALLNUT, IMAGE_REPEASHOOTER, IMAGE_POTATOMINE, IMAGE_PEABULLET, IMAGE_SNOWPEABULLET, IMAGE_GROWSOIL, IMAGE_POTATOMINE_MASHED, IMAGE_POTATOMINE_BOOM,\
                           WAV_POTATO_BOOM, WAV_DIRT_RISE, WAV_KILL_PLANT, WAV_PLANT
from game_sunlight import SunLight_Plant
from game_bullet import PeaBullet, SnowBullet

#植物父类
class _Plant():
    def __init__(self, kind,size):
        self.image_index = 0
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.fps = 5

        self.blood = GAME_PLANT_BLOOD[kind]
        self.atk = GAME_PLANT_ATK[kind]

        self.is_first = True   #第一个是否有特性

        self.bullet_num = -1   #子弹连发数
        self.bullets = None

        self.shovel_kill =  False
        self.self_kill = False

    #射击逻辑
    def fire(self, bullet_kind, bullet_image, zombies, bullet_nums = 1):
        for zombie in zombies:
            #射击判断
            if not (self.rect.centery >= zombie.rect.centery and self.rect.centery <= zombie.rect.centery + 35 and zombie.rect.centerx <= WIDTH and self.rect.centerx <= zombie.rect.centerx):continue

            #延迟判断
            now = game_config.FRAMECOUNT
            clip = [True for _ in range(bullet_nums-1)] + [False]
            fire_delay = 0 if self.is_first else PeaBullet.peafire_delay_short() if clip[self.bullet_num] else random.uniform(PeaBullet.peafire_delay_long()[0], PeaBullet.peafire_delay_long()[1])

            #攻击判断
            if now - self.last_fire >= fire_delay:
                bullet = bullet_kind(bullet_image, self.atk, (self.rect.centerx, self.rect.top))
                bullet.add(self.bullets)
                self.alls_sprites.add(bullet, layer=3)
                self.last_fire = now if self.is_first else now if self.bullet_num != bullet_nums-2 else now - PeaBullet.peafire_delay_short() * (bullet_nums - 1)
                self.is_first = False
                self.bullet_num = (self.bullet_num + 1) % bullet_nums

    #采用植物自己的fps
    def refresh(self):
        return game_config.FRAMECOUNT % self.fps == 0

    #攻击--抽象方法
    def attack_zombie(self, zombies):
        pass

    def update(self):
        game_config.PLANT_POS[self.rect.center] = True
        if self.blood <= 0:
            if self.shovel_kill:
                random.choice(WAV_PLANT).play()
            elif self.self_kill:
                None
            else:
                WAV_KILL_PLANT.play()
            game_config.PLANT_POS[self.rect.center] = False
            self.kill()

#太阳花--子类
class SunFlower(pygame.sprite.Sprite, _Plant):
    def __init__(self, pos, alls, sun):
        super().__init__()
        _Plant.__init__(self, "SunFlower", (73, 74))

        self.alls_sprites = alls
        self.sun = sun

        self.is_ready = 0  #准备好时植物高亮图片组的索引为1

        self.image = IMAGE_SUNFLOWER[self.is_ready][self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
        self.light_time = 0                          #高亮的起始时间
        self.light_delaytime = 90                    #高亮时间
        self.last_sun = game_config.FRAMECOUNT       #产生阳光的时间
    
    #产生阳光
    def bornsun(self):
        #产生延迟判断
        bornsun_delay = SunLight_Plant.delay_plant()[0] if self.is_first else SunLight_Plant.delay_plant()[1]

        #产生阳光判断
        now_1 = game_config.FRAMECOUNT
        self.light_time = game_config.FRAMECOUNT if self.is_ready == 0 else self.light_time
        if now_1 - self.last_sun < random.uniform(bornsun_delay[0]-self.light_delaytime, bornsun_delay[1]-self.light_delaytime):return

        self.is_ready = 1
        now_2 = game_config.FRAMECOUNT
        #高亮是否结束--结束后产生阳光
        if now_2 - self.light_time >= self.light_delaytime:
            self.is_ready = 0
            sunlight = SunLight_Plant(self.rect.center)
            sunlight.add(self.sun)
            self.alls_sprites.add(sunlight, layer=6)
            self.last_sun = now_2
            self.is_first = False

    def update(self):
        if not self.refresh(): return
        _Plant.update(self)
        self.bornsun()
        self.image_index = (self.image_index + 1) % len(IMAGE_SUNFLOWER[0])
        self.image = IMAGE_SUNFLOWER[self.is_ready][self.image_index]

#豌豆射手--子类
class PeaShooter(pygame.sprite.Sprite, _Plant):
    def __init__(self, pos, alls):
        super().__init__()
        _Plant.__init__(self, "PeaShooter", (71, 71))

        self.alls_sprites = alls
        self.bullets = pygame.sprite.Group()

        self.image = IMAGE_PEASHOOTER[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.last_fire = game_config.FRAMECOUNT         #射击时间
        
    def attack_zombie(self, zombies):
        self.fire(PeaBullet, IMAGE_PEABULLET, zombies)
        for bullet in self.bullets:
            bullet.hit_zombie(zombies)

    def update(self):
        if not self.refresh(): return
        _Plant.update(self)
        self.image_index = (self.image_index + 1) % len(IMAGE_PEASHOOTER)
        self.image = IMAGE_PEASHOOTER[self.image_index]

#寒冰射手--子类
class SnowPeaShooter(pygame.sprite.Sprite, _Plant):
    def __init__(self, pos, alls):
        super().__init__()
        _Plant.__init__(self, "SnowPeaShooter", (71, 71))

        self.alls_sprites = alls
        self.bullets = pygame.sprite.Group()

        self.image = IMAGE_SNOWPEASHOOTER[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.last_fire = game_config.FRAMECOUNT

    def attack_zombie(self, zombies):
        self.fire(SnowBullet, IMAGE_SNOWPEABULLET, zombies)
        for bullet in self.bullets:
            bullet.hit_zombie(zombies)

    def update(self):
        if not self.refresh(): return
        _Plant.update(self)
        self.image_index = (self.image_index + 1) % len(IMAGE_SNOWPEASHOOTER)
        self.image = IMAGE_SNOWPEASHOOTER[self.image_index]

#双发豌豆--子类
class RePeaShooter(pygame.sprite.Sprite, _Plant):
    def __init__(self, pos, alls):
        super().__init__()
        _Plant.__init__(self, "RePeaShooter", (73, 71))

        self.alls_sprites = alls
        self.bullets = pygame.sprite.Group()

        self.image = IMAGE_REPEASHOOTER[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
        self.bullet_nums = 2                       #连发数=2
        self.last_fire = game_config.FRAMECOUNT

    def attack_zombie(self, zombies):
        self.fire(PeaBullet, IMAGE_PEABULLET, zombies, self.bullet_nums)
        for bullet in self.bullets:
            bullet.hit_zombie(zombies)
    
    def update(self):
        if not self.refresh(): return
        _Plant.update(self)
        self.image_index = (self.image_index + 1) % len(IMAGE_REPEASHOOTER)
        self.image = IMAGE_REPEASHOOTER[self.image_index]

#坚果墙--子类
class WallNut(pygame.sprite.Sprite, _Plant):
    def __init__(self, pos):
        super().__init__()
        _Plant.__init__(self, "WallNut", (65, 73))

        self.health = 0           #血量状态
        self.image = IMAGE_WALLNUT[self.health][self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        if not self.refresh(): return
        _Plant.update(self)
        self.health = 2 if self.blood <= 1333 else 1 if self.blood <= 2666 else 0
        self.image_index = (self.image_index + 1) % len(IMAGE_WALLNUT[0])
        self.image = IMAGE_WALLNUT[self.health][self.image_index]

#土豆地雷--子类
class PotatoMine(pygame.sprite.Sprite, _Plant):
    
    #土壤特效
    class GrowSoil(pygame.sprite.Sprite):
        def __init__(self, center):
            super().__init__()

            self.size = (IMAGE_GROWSOIL[0].get_width() * 2, IMAGE_GROWSOIL[0].get_height() * 2)    #将土壤图片设置为原图片的2倍

            self.soil_index = 0
            self.image = pygame.transform.scale(IMAGE_GROWSOIL[self.soil_index], self.size)
            self.rect = self.image.get_rect()
            self.rect.center = center

        def update(self):
            self.soil_index = (self.soil_index + 1) % len(IMAGE_GROWSOIL)
            self.image = IMAGE_GROWSOIL[self.soil_index]
            if self.soil_index + 1 == len(IMAGE_GROWSOIL):self.kill()              #当土壤图片全部索引完后kill
    
    #爆炸特效
    class Boom(pygame.sprite.Sprite):
        def __init__(self, center):
            super().__init__()

            self.image = IMAGE_POTATOMINE_BOOM
            self.rect = self.image.get_rect()
            self.rect.center = center

            self.boom_dealy = 15                 #爆炸存在时间
            self.start = game_config.FRAMECOUNT  #爆炸开始时间

        def update(self):
            now = game_config.FRAMECOUNT
            if now - self.start > self.boom_dealy:self.kill()     #爆炸开始短暂延迟后kill

    def __init__(self, pos, alls):
        super().__init__()
        _Plant.__init__(self, "PotatoMine", (75, 55))

        self.alls_sprites = alls

        self.up = 0     #0为未出土 / 1为以出土
        self.image = IMAGE_POTATOMINE[self.up][self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.boom_sprite = None
        self.self_kill = True
        
        self.is_boom = False                       #是否爆炸
        self.boom_time = game_config.FRAMECOUNT    #爆炸时间
        self.plant = game_config.FRAMECOUNT        #种植时间

        self.boom_range = 150       #爆炸范围
        self.ready_time = 900     #出土延迟

    #出土判断
    def come_up(self):
        now = game_config.FRAMECOUNT
        if now - self.plant < self.ready_time:return

        if self.up == 0:
            WAV_DIRT_RISE.play()
            PotatoMine.GrowSoil((self.rect.centerx, self.rect.top)).add(self.alls_sprites)
        self.up = 1

    #自定义碰撞检测方式
    def collide(self, sprite1, sprite2):
        if sprite1.rect.collidepoint((sprite2.rect.left + 90, sprite2.rect.top + 90)) or sprite1.rect.collidepoint((sprite2.rect.left + 150, sprite2.rect.top + 90)):return True
        return False
    
    #炸僵尸！
    def attack_zombie(self, zombies):
        zombie = pygame.sprite.spritecollideany(self, zombies, collided=self.collide)
        #爆炸条件--僵尸碰撞、已出土
        if zombie and self.up == 1:
            if not self.is_boom:
                WAV_POTATO_BOOM.play()
                self.boom_sprite = PotatoMine.Boom((self.rect.centerx, self.rect.top - 50))
                self.boom_sprite.add(self.alls_sprites)
                self.is_boom = True
                self.blood = 0
            #检测在爆炸范围内的僵尸
            for zombie in zombies:
                if (self.rect.centerx - zombie.rect.centerx) ** 2 + (self.rect.centery - zombie.rect.centery) ** 2 <= self.boom_range ** 2:
                    zombie.blood -= self.atk
                    zombie.is_boom = True

    def update(self):
        if not self.refresh(): return
        _Plant.update(self)

        #爆炸开始短暂延迟后kill
        if not self.is_boom:self.boom_time = game_config.FRAMECOUNT
        now = game_config.FRAMECOUNT
        if now - self.boom_time > 15:self.kill()

        self.come_up()
        self.image_index = (self.image_index + 1) % len(IMAGE_POTATOMINE[self.up])
        self.image = IMAGE_POTATOMINE[self.up][self.image_index] if self.is_boom == False else IMAGE_POTATOMINE_MASHED
        self.rect = self.image.get_rect(center=self.rect.center)

#314