import pygame

#游戏基础配置
WIDTH, HEIGHT = 800, 600                            #窗口大小
GAMETITLE = "植物大战僵尸-青春版"                     #游戏标题
GAMEFPS = 60                                        #游戏主帧率
FRAMECOUNT = 0                                      #帧数计数器

#游戏关卡配置
GAME_SUNNUMS = 50                                                                      #初始阳光数
PLANT_POS = {(80 * i, 125 + 100*j):False for i in range(1, 10) for j in range(5)}      #种植位置

#列表第一行信息:生成僵尸宽度, 该僵尸移动速度, 前n-1波的长度占比(可以优化成关卡类)
PASS_1 = [[[(0, 15, 45)]],\
          [[(845, 180)],\
           [(1077, 275), (1077, 385), (1302, 180), (1302, 385), (1730, 275), (1932, 465)],\
           [(1302, 575), (1520, 465), (1730, 180), (1932, 385), (2315, 465)],\
           [(1520, 275), (1932, 575), (2122, 275)]],\
          [[(950, 385)],\
           [(972, 385),(972, 465), (1085, 275), (1085, 465), (1190, 385), (1190, 575), (1287, 180), (1460, 180),\
            (1460, 385), (1535, 385), (1535, 465), (1617, 465), (1617, 565), (1790, 565), (1865, 180)],\
           [(972, 275), (972, 575),(1190, 180), (1287, 575),\
            (1460, 275), (1535, 575), (1707, 385), (1865, 385)],\
           [(1085, 385), (1287, 275), (1377, 465), (1617, 180),\
            (1790, 180), (1865, 575)]]]

#植物配置
GAME_PLANT_BLOOD = {"SunFlower":300, "PeaShooter":300, "SnowPeaShooter":300, "RePeaShooter":300, "WallNut":4000, "PotatoMine":300}     #植物血量
GAME_PLANT_ATK = {"SunFlower":0, "PeaShooter":20, "SnowPeaShooter":20, "RePeaShooter":20, "WallNut":0, "PotatoMine":1800}              #植物攻击力
GAME_PLANT_PRICE = {"SunFlower":50, "PeaShooter":100, "SnowPeaShooter":175, "RePeaShooter":200, "WallNut":50, "PotatoMine":25}         #植物价格
GAME_PLANT_CD = {"SunFlower":450, "PeaShooter":450, "SnowPeaShooter":450, "RePeaShooter":450, "WallNut":1800, "PotatoMine":1800}       #植物冷却时间

#僵尸配置
GAME_ZOMBIE_BLOOD = {"Zombie":270, "FlagZombie":270, "ConeheadZombie":640, "BucketheadZombie":1370}             #僵尸血量
GAME_ZOMBIE_ATK = {"Zombie":2.5, "FlagZombie":2.5, "ConeheadZombie":2.5, "BucketheadZombie":2.5}                #僵尸攻击力
GAME_ZOMBIE_SPEED = {"Zombie":2, "FlagZombie":4, "ConeheadZombie":2, "BucketheadZombie":2}                      #僵尸速度

#按键配置
GAME_KEYS = {"pause":pygame.K_SPACE}

#游戏结束事件
EVENT_GAME_OVER = pygame.USEREVENT   