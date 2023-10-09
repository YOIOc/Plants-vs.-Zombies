import pygame
import game_config
from game_config import WIDTH, HEIGHT
from game_config import WIDTH
from game_resources import IMAGE_CAEDFIELD, IMAGE_LAWNCLEANER, IMAGE_SHOVEL, IMAGE_SHOVELSLOT, IMAGE_FIAGEMETER_EMPTY,\
                           WAV_IST_SHOVEL, WAV_IS_SHOVEL

#卡片栏
class CardField(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = IMAGE_CAEDFIELD
        self.rect = self.image.get_rect()
        self.rect.topleft = 10, 0

        pygame.Surface.set_colorkey(self.image, "white")   #透明图片中的白色区域

    @staticmethod
    def cardfield_pos():
        return 10, 0

#当前阳光数
class SunNums(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.font_size = 25
        self.font = pygame.font.Font(None, self.font_size)
        self.image = self.font.render(f"{game_config.GAME_SUNNUMS}", True, "black")
        self.rect = self.image.get_rect()
        self.rect.center = CardField.cardfield_pos()[0] + 40, CardField.cardfield_pos()[1] + 73

    def update(self):
        self.image = self.font.render(f"{game_config.GAME_SUNNUMS}", True, "black")
        self.rect = self.image.get_rect(center = self.rect.center)

#铲子栏
class ShovelSlot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = IMAGE_SHOVELSLOT
        self.rect = self.image.get_rect()
        self.rect.topleft = CardField.cardfield_pos()[0] + 522, CardField.cardfield_pos()[1]

#铲子
class Shovel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = IMAGE_SHOVEL
        self.rect = self.image.get_rect()
        self.rect.topleft = CardField.cardfield_pos()[0] + 522, CardField.cardfield_pos()[1]

        self.is_selected = False

    #是否点击了铲子
    def handle_event(self, events, is_use_mouse):
        for e in events:
            #使用铲子
            if not self.is_selected and e.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(e.pos) and not is_use_mouse:
                WAV_IS_SHOVEL.play()
                self.is_selected = True
            #归还铲子
            elif self.is_selected and e.type == pygame.MOUSEBUTTONUP:
                WAV_IST_SHOVEL.play()
                self.is_selected = False

    #检查鼠标是否被使用
    def is_use_mouse(self):
        return self.is_selected

    def update(self):
        if self.is_selected:
            self.rect.bottomleft = pygame.mouse.get_pos()
            return
        self.rect.topleft = CardField.cardfield_pos()[0] + 522, CardField.cardfield_pos()[1]

#割草机
class LawnCleaner(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()

        self.image = IMAGE_LAWNCLEANER
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.speed = 0   #移动速度

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()

#关卡进度--背景
class FlagMeter_Background(pygame.sprite.Sprite):
    #关卡进程图片
    class LevelProgress(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()

            self.image = IMAGE_FIAGEMETER_EMPTY[1]
            self.rect = self.image.get_rect()
            self.rect.bottom, self.rect.centerx = HEIGHT, FlagMeter_Background.flagmeter()[0] + FlagMeter_Background.flagmeter()[2] / 2

    def __init__(self):
        super().__init__()

        self.image = IMAGE_FIAGEMETER_EMPTY[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = 600, 575

    #游戏进度UI的位置
    @staticmethod
    def flagmeter():
        return 600, 575, 157, 21
    #僵尸头的初始位置
    @staticmethod
    def zombiehead_pos():
        return 751, 585
    #旗子的y轴坐标
    @staticmethod
    def flag_bottom():
        return 592
    #进度条的x, y, width, height
    staticmethod
    def progress_bar():
        return 606, 575, 145, 21

#进度条精灵
class FlagMeterFull(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.progress_bar = FlagMeter_Background.progress_bar() #进度条rect

        self.image = pygame.Surface((self.progress_bar[2], self.progress_bar[3]), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.progress_bar[0], self.progress_bar[1]

    def move(self, speed):
        self.image.blit(IMAGE_FIAGEMETER_EMPTY[4], (self.progress_bar[2] - speed, 0))

#僵尸头精灵
class ZombieHead(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = IMAGE_FIAGEMETER_EMPTY[3]
        self.rect = self.image.get_rect()
        self.rect.center = FlagMeter_Background.zombiehead_pos()
        self.centerx = FlagMeter_Background.zombiehead_pos()[0] - 4  #因为小数像素无法体现，存在误差，故加上了4像素的误差

        self.speed = 0

    def move(self, speed):
        self.rect.centerx = self.centerx - speed

#旗子精灵
class FlagMeterFlag(pygame.sprite.Sprite):
    def __init__(self, left):
        super().__init__()

        self.image = IMAGE_FIAGEMETER_EMPTY[2]
        self.rect = self.image.get_rect()
        self.rect.centerx = left
        self.rect.bottom = FlagMeter_Background.flag_bottom()

        self.fps = 4
        self.flag_speed = 0

    #新一波开始
    def next_wave(self, zombiehead_rect):
        if self.rect.colliderect(zombiehead_rect):
            self.flag_speed = 1

    def update(self):
        if game_config.FRAMECOUNT % self.fps != 0:return
        if self.rect.bottom + 14 < FlagMeter_Background.flag_bottom():return
        self.rect.top -= self.flag_speed

#181