import pygame
import random
import game_config
from game_config import GAME_PLANT_PRICE, GAME_PLANT_CD, PLANT_POS
from game_resources import IMAGE_CARDS, IMAGE_SUNFLOWER, IMAGE_PEASHOOTER, IMAGE_SNOWPEASHOOTER, IMAGE_REPEASHOOTER, IMAGE_WALLNUT, IMAGE_POTATOMINE,\
                           WAV_PLANT, WAV_CHEECKD_CARD
from game_plant import SunFlower, PeaShooter, SnowPeaShooter, RePeaShooter, WallNut, PotatoMine
from game_ui import CardField

#卡片父类
class _Card():

    #该卡片对应的植物
    class Card_Plant(pygame.sprite.Sprite):
        def __init__(self, plant_image, follow_mouse, pos = None):
            super().__init__()

            self.follow_mouse = follow_mouse   #是否跟随鼠标
            self.pos = pos

            self.follow_mouse_plant = plant_image            #跟随鼠标的图片
            self.location_prompt_plant = plant_image.copy()  #位置提示的图片
            self.location_prompt_plant.set_alpha(120)        #设置位置提示植物的透明度

            self.image = self.follow_mouse_plant if self.follow_mouse else self.location_prompt_plant
            self.rect = self.image.get_rect()
            self.rect.center = pygame.mouse.get_pos() if self.follow_mouse else self.pos

        def update(self):
            if self.follow_mouse:self.rect.center = pygame.mouse.get_pos()
        
    def __init__(self, kind, alls):
        self.alls = alls

        self.image = pygame.Surface((48, 68))
        self.image_light = pygame.Surface((48, 68))    #彩色卡片
        self.image_gray = pygame.Surface((48, 68))     #灰色卡片
        self.rect = self.image.get_rect()
        self.image_plant = None

        self.init_y = 1                          #阴影覆盖的y轴坐标
        self.shadow = pygame.Surface((48, 68), pygame.SRCALPHA)
        self.shadow.fill((0, 0, 0, 125))

        self.price = GAME_PLANT_PRICE[kind]
        self.cd = GAME_PLANT_CD[kind]

        #条件参数
        self.cd_frame = 1             #已冷却时间       
        self.is_ready = False         #是否准备好
        self.is_selected = False      #是否被选中
        self.is_grow_plant = False    #是否种植了植物
        self.is_shadow = False        #是否覆盖阴影

        #植物实例
        self.follow_mouse_plant = None      #跟随鼠标的植物实例
        self.location_prompt_plant = None   #位置提示的植物实例

    #判断是否能种植
    def judge_ready(self):
        if not self.is_shadow and game_config.GAME_SUNNUMS >= self.price:
            self.is_ready = True
        else:
            self.is_ready = False

    #是否被选中、种植
    def handle_event(self, events, is_use_mouse):
        for e in events:
            #被选中
            if self.is_ready and not self.is_selected and e.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(e.pos) and not is_use_mouse:
                WAV_CHEECKD_CARD.play()
                self.is_selected = True
            #取消选中
            elif self.is_selected and e.type == pygame.MOUSEBUTTONDOWN:
                self.is_selected = False
            #被种植
            if self.location_prompt_plant and e.type == pygame.MOUSEBUTTONDOWN:
                self.is_grow_plant = True

    #跟随鼠标
    def follow_mouse(self):
        #实例选中卡片的跟随植物
        if self.is_selected and self.follow_mouse_plant == None:
            self.follow_mouse_plant = _Card.Card_Plant(self.image_plant, True)
            self.follow_mouse_plant.add(self.alls)
        #删除跟随鼠标的实例
        elif not self.is_selected and self.follow_mouse_plant:
            self.follow_mouse_plant.kill()
            self.follow_mouse_plant = None

    #位置提示的判断范围
    def location_prompt_range(self, pos):
        return pygame.mouse.get_pos()[0] in range(pos[0] - 40, pos[0] + 41) and pygame.mouse.get_pos()[1] in range(pos[1] - 50, pos[1] + 51)
    
    #位置提示
    def location_prompt(self):
        if self.follow_mouse_plant and self.location_prompt_plant == None:
            for pos, state in PLANT_POS.items():
                #实例位置提示的植物
                if self.location_prompt_range(pos) and not state:
                    self.location_prompt_plant = _Card.Card_Plant(self.image_plant, False, pos)
                    self.location_prompt_plant.add(self.alls)
        if self.location_prompt_plant:
            #删除位置提示的实例
            if not self.location_prompt_range(self.location_prompt_plant.pos) or self.follow_mouse_plant == None:
                self.location_prompt_plant.kill()
                self.location_prompt_plant = None

    #种植植物
    def grow_plant(self, plants):
        if self.is_grow_plant:
            random.choice(WAV_PLANT).play()
            plant = self.plant()
            plant.add(self.alls, plants)
            self.alls.add(plant, layer=2)
            self.is_grow_plant = False
            game_config.GAME_SUNNUMS -= self.price
            self.cd_frame = 0
            self.is_shadow = True

    #更新卡片动画
    def update_image(self):
        if self.is_ready:
            self.init_y = 1
            self.image.blit(self.image_light, (0, 0))
        else:
            if not self.is_shadow:
                self.image.blit(self.image_gray, (0, 0))
                return
            self.cd_frame += 1
            if self.cd_frame < self.cd:
                self.init_y = -(68*self.cd_frame/self.cd)
            elif self.cd_frame == self.cd:
                self.cd_frame = 0
                self.is_shadow = False

            self.image.fill((0, 0, 0, 0))
            self.image.blit(self.image_gray, (0, 0))
            self.image.blit(self.shadow, (0, self.init_y))

    #检查鼠标是否被使用
    def is_use_mouse(self):
        return self.is_selected

    def update(self):
        self.judge_ready()
        self.update_image()
        self.follow_mouse()
        self.location_prompt()
        
#太阳花卡片--子类
class SunFlowerCard(pygame.sprite.Sprite, _Card):
    def __init__(self, alls, sun):
        super().__init__()
        _Card.__init__(self, "SunFlower", alls, )

        self.sun = sun

        self.image_light.blit(IMAGE_CARDS[0], (0,0))
        self.image_gray = IMAGE_CARDS[1]
        self.rect = self.image.get_rect()
        self.image_plant = IMAGE_SUNFLOWER[0][0]
        self.rect.topleft = CardField.cardfield_pos()[0] + 82, CardField.cardfield_pos()[1] + 9 

        self.is_shadow = False

    def plant(self):
        return SunFlower(self.location_prompt_plant.pos, self.alls, self.sun)

    def update(self):
        _Card.update(self)

#豌豆射手卡片--子类
class PeaShooterCard(pygame.sprite.Sprite, _Card):
    def __init__(self, alls):
        super().__init__()
        _Card.__init__(self, "PeaShooter", alls)

        self.image_light = IMAGE_CARDS[2]
        self.image_gray = IMAGE_CARDS[3]
        self.rect = self.image.get_rect()
        self.image_plant = IMAGE_PEASHOOTER[0]
        self.rect.topleft = CardField.cardfield_pos()[0] + 136, CardField.cardfield_pos()[1] + 9

        self.is_shadow = False

    def plant(self):
        return PeaShooter(self.location_prompt_plant.pos, self.alls)

    def update(self):
        _Card.update(self)

#寒冰射手卡片--子类
class SnowPeaShooterCard(pygame.sprite.Sprite, _Card):
    def __init__(self, alls):
        super().__init__()
        _Card.__init__(self, "SnowPeaShooter", alls)

        self.image_light = IMAGE_CARDS[4]
        self.image_gray = IMAGE_CARDS[5]
        self.rect = self.image.get_rect()
        self.image_plant = IMAGE_SNOWPEASHOOTER[0]
        self.rect.topleft = CardField.cardfield_pos()[0] + 190, CardField.cardfield_pos()[1] + 9

        self.is_shadow = False

    def plant(self):
        return SnowPeaShooter(self.location_prompt_plant.pos, self.alls)

    def update(self):
        _Card.update(self)

#双发豌豆卡片--子类
class RePeaShooterCard(pygame.sprite.Sprite, _Card):
    def __init__(self, alls):
        super().__init__()
        _Card.__init__(self, "RePeaShooter", alls)

        self.image_light = IMAGE_CARDS[6]
        self.image_gray = IMAGE_CARDS[7]
        self.rect = self.image.get_rect()
        self.image_plant = IMAGE_REPEASHOOTER[0]
        self.rect.topleft = CardField.cardfield_pos()[0] + 244, CardField.cardfield_pos()[1] + 9

        self.is_shadow = False

    def plant(self):
        return RePeaShooter(self.location_prompt_plant.pos, self.alls)

    def update(self):
        _Card.update(self)

#坚果墙卡片--子类
class WallNutCard(pygame.sprite.Sprite, _Card):
    def __init__(self, alls):
        super().__init__()
        _Card.__init__(self, "WallNut", alls)

        self.image_light = IMAGE_CARDS[8]
        self.image_gray = IMAGE_CARDS[9]
        self.rect = self.image.get_rect()
        self.image_plant = IMAGE_WALLNUT[0][0]
        self.rect.topleft = CardField.cardfield_pos()[0] + 298, CardField.cardfield_pos()[1] + 9

        self.is_shadow = True

    def plant(self):
        return WallNut(self.location_prompt_plant.pos)

    def update(self):
        _Card.update(self)

#土豆地雷卡片--子类
class PotatoMineCard(pygame.sprite.Sprite, _Card):
    def __init__(self, alls):
        super().__init__()
        _Card.__init__(self, "PotatoMine", alls)

        self.image_light = IMAGE_CARDS[10]
        self.image_gray = IMAGE_CARDS[11]
        self.rect = self.image.get_rect()
        self.image_plant = IMAGE_POTATOMINE[1][0]
        self.rect.topleft = CardField.cardfield_pos()[0] + 352, CardField.cardfield_pos()[1] + 9

        self.is_shadow = True

    def plant(self):
        return PotatoMine(self.location_prompt_plant.pos, self.alls)

    def update(self):
        _Card.update(self)

#271