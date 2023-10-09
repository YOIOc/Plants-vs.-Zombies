import pygame
import game_config
from  game_config import PASS_1, EVENT_GAME_OVER
from game_resources import WAV_CHEECKD_CARD
from game_background import Background
from game_sunlight import SunLight_Sky
from game_ui import CardField, SunNums, LawnCleaner, ShovelSlot, Shovel, FlagMeter_Background, FlagMeterFull, FlagMeterFlag, ZombieHead
from game_card import SunFlowerCard, PeaShooterCard, SnowPeaShooterCard, RePeaShooterCard, WallNutCard, PotatoMineCard
from game_zombie import Zombie, FlagZombie, ConeheadZombie, BucketheadZombie
from game_condition import Start_Wave, Middle_Wave, End_Wave

#游戏服务器
class GameServer:
    def __init__(self):
        self.start()

    def start(self):
        #创建各精灵组
        #     all_sprites中的图层顺序:铲子
        #第一层(默认)：背景、卡片栏、阳光数、铲子框、割草机
        #第二层：卡片、植物
        #第三层：僵尸
        #第四层：铲子、子弹
        #第五层：阳光
        #第六层：动画、背景条、进度条、僵尸头、小旗
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.plants = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()
        self.suns = pygame.sprite.Group()
        self.flags = pygame.sprite.Group()
        self.lawncleaners = pygame.sprite.Group()
        self.cards = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()

        #添加背景精灵
        self.all_sprites.add(Background())
        
        #添加UI精灵
        CardField().add(self.all_sprites)
        SunNums().add(self.all_sprites)
        ShovelSlot().add(self.all_sprites)
        self.shovel = Shovel()
        self.all_sprites.add(self.shovel, layer=3)
        # self.append_sprites_group(Shovel(), 4)
        self.set_lawncleaner()

        self.flagmeter_background = FlagMeter_Background()
        self.all_sprites.add(self.flagmeter_background, layer=7)
        # self.append_sprites_group(self.flagmeter_background, 7)                #关卡进度背景1
        self.full = FlagMeterFull()
        self.all_sprites.add(self.full, layer=7)
        # self.append_sprites_group(self.full, 7)                                #关卡进度条
        self.set_flag(PASS_1)                                                    #关卡小旗
        self.all_sprites.add(self.flagmeter_background.LevelProgress(), layer=7) #关卡进度背景2
        # self.append_sprites_group(self.flagmeter_background.LevelProgress(), 7)
        self.zombiehead = ZombieHead()
        self.all_sprites.add(self.zombiehead, layer=7)                              #僵尸头
        # self.append_sprites_group(self.zombiehead, 7)

        #添加植物卡片精灵
        SunFlowerCard(self.all_sprites, self.suns).add(self.all_sprites, self.cards)
        PeaShooterCard(self.all_sprites).add(self.all_sprites, self.cards)
        SnowPeaShooterCard(self.all_sprites).add(self.all_sprites, self.cards)
        RePeaShooterCard(self.all_sprites).add(self.all_sprites, self.cards)
        WallNutCard(self.all_sprites).add(self.all_sprites, self.cards)
        PeaShooterCard(self.all_sprites).add(self.all_sprites, self.cards)
        PotatoMineCard(self.all_sprites).add(self.all_sprites, self.cards)

        #关卡信息
        self.wave = 1
        self.zombie_dienums = 0
        self.game_progres = 0
        
        #飘落阳光的时间
        self.start_sun = game_config.FRAMECOUNT

        #第一波动画
        self.first_car = None

    #设置割草机
    def set_lawncleaner(self):
        for i in range(5):
            lawncleaner = LawnCleaner((8, 145 + i * 100))
            self.lawncleaners.add(lawncleaner)
            self.all_sprites.add(lawncleaner, layer=3)
            # self.append_sprites_group(LawnCleaner((8, 145 + i * 100)), 3, self.lawncleaners)

    #设置波次小旗
    def set_flag(self, game_pass):
        flag_left = FlagMeter_Background.flagmeter()[0] + FlagMeter_Background.progress_bar()[2] + 0
        for i in range(len(game_pass) - 2):
            wavelength_ratio = game_pass[0][0][0][i+1] / game_pass[0][0][0][-1]
            wave_progress_bar_width = int(FlagMeter_Background.progress_bar()[2] * wavelength_ratio)
            flag = FlagMeterFlag(flag_left - wave_progress_bar_width)
            self.flags.add(flag)
            self.all_sprites.add(flag, layer=7)
            # self.append_sprites_group(FlagMeterFlag(flag_left - wave_progress_bar_width), 7, self.flags)

    #更新游戏波次
    def update_wave(self):
        if not (len(self.zombies) == 0 and self.wave <= len(PASS_1) - 1):return

        self.update_waveprompt()
        self.update_flag()
        self.born_zombies()
        self.wave += 1

    #波次开场动画
    def update_waveprompt(self):
        if self.wave == 1:
            self.first_car = Start_Wave()
            self.first_car.add(self.cars)
        elif self.wave != 1 and self.wave != len(PASS_1) - 1:
            Middle_Wave().add(self.cars)
        else:
            End_Wave().add(self.cars)

    #飘落阳光
    def born_suns(self):
        now = game_config.FRAMECOUNT
        if now - self.start_sun < SunLight_Sky.delay_sky():return

        sunlight = SunLight_Sky()
        sunlight.add(self.suns)
        self.all_sprites.add(sunlight, layer=6)
        self.start_sun = now

    #种植植物
    def born_plants(self):
        for card in self.cards:
            card.grow_plant(self.plants)

    #产生僵尸
    def born_zombies(self):
        for kind in range(4):
            for pos in PASS_1[self.wave][kind]:
                if kind == 0:
                    zombie = FlagZombie(self.all_sprites, pos)
                    self.zombies.add(zombie)
                    self.all_sprites.add(zombie, layer=4)
                elif kind == 1:
                    zombie = Zombie(self.all_sprites, pos)
                    self.zombies.add(zombie)
                    self.all_sprites.add(zombie, layer=4)
                elif kind == 2:
                    zombie = ConeheadZombie(self.all_sprites, pos)
                    self.zombies.add(zombie)
                    self.all_sprites.add(zombie, layer=4)
                elif kind == 3:
                    zombie = BucketheadZombie(self.all_sprites, pos)
                    self.zombies.add(zombie)
                    self.all_sprites.add(zombie, layer=4)
                    # self.append_sprites_group(BucketheadZombie(self.all_sprites, pos), 2, self.zombies)
                    
    #更新关卡进度
    def refresh_zombiehead_pos(self):
        self.zombie_dienums = PASS_1[0][0][0][self.wave-1] - len(self.zombies)
        self.game_progres = self.zombie_dienums * (FlagMeter_Background.progress_bar()[2] // PASS_1[0][0][0][-1])
        self.zombiehead.move(self.game_progres)
        self.full.move(self.game_progres)

    #小旗动画
    def update_flag(self):
        for flag in self.flags:
            flag.next_wave(self.zombiehead.rect)

    #铲子铲除植物
    def shove_kill_plant(self):
        if not self.shovel.is_selected:return

        for plant in self.plants:
            if pygame.mouse.get_pressed()[0] and plant.rect.collidepoint(pygame.mouse.get_pos()):
                WAV_CHEECKD_CARD.play()
                plant.shovel_kill = True
                plant.blood = 0

    #植物攻击僵尸
    def attack_zombie(self):
        for plant in self.plants:
            plant.attack_zombie(self.zombies)

    #僵尸碰撞
    def zombie_hit(self):
        self.eat_plant()
        self.hit_lawncleaner()

    #僵尸吃植物
    def eat_plant(self):
        for zombie in self.zombies:
            zombie.eat_plant(self.plants)

    #僵尸撞击小车
    def hit_lawncleaner(self):
        for zombie in self.zombies:
            zombie.hit_lawncleaner(self.lawncleaners)

    #需要设置图层顺序的精灵添加方法
    def append_sprites_group(self, sprite, layer=0, other_group=None):
        add_sprite = sprite
        if other_group:
            other_group.add(add_sprite)
        self.all_sprites.add(add_sprite, layer=layer)

    #检查鼠标是否被使用
    def is_use_mouse(self):
        for sun in self.suns:
            if sun.is_use_mouse():return True
        for card in self.cards:
            if card.is_use_mouse():return True
        if self.shovel.is_use_mouse():return True
        return False

    #游戏结束事件
    def over_game(self):
        if self.zombie_dienums == PASS_1[0][0][0][-1]:
            e = pygame.event.Event(EVENT_GAME_OVER, {"state":True})        #创建获胜结束事件
            pygame.event.post(e)
        for zombie in self.zombies:
            if zombie.rect.right < 0:
                e = pygame.event.Event(EVENT_GAME_OVER, {"state":False})   #创建失败结束事件
                pygame.event.post(e)

    def draw(self, surf):
        self.all_sprites.draw(surf)
        self.cars.draw(surf)

    def update(self):
        self.cars.update()
        if self.cars.has(self.first_car):return
        self.born_suns()
        self.born_plants()
        self.update_wave()
        self.refresh_zombiehead_pos()
        self.shove_kill_plant()
        self.attack_zombie()
        self.zombie_hit()
        self.over_game()
        self.all_sprites.update()

    def handle_event(self):
        events = pygame.event.get()
        for sun in self.suns:
            sun.handle_event(events, self.is_use_mouse())

        for card in self.cards:
            card.handle_event(events, self.is_use_mouse())

        self.shovel.handle_event(events, self.is_use_mouse())

#251