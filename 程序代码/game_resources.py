import os
import pygame
from game_config import GAME_PLANT_BLOOD

#加载图片资源
def load_img_resources(filename):
    fullname = os.path.join(img_dir, filename)
    try:
        resources = pygame.image.load(fullname)
    except:
        raise ValueError(f"找不到对应文件:{fullname}")
    return resources

#加载音频资源
def load_wav_resources(filename):
    fullname = os.path.join(wav_dir, filename)
    try:
        resources = pygame.mixer.Sound(fullname)
    except:
        raise ValueError(f"找不到对应文件:{fullname}")
    return resources

#加载需要剪切的图片资源
def split_image(filename, rows, cols):
    fullname = os.path.join(img_dir, filename)
    src_img = pygame.image.load(fullname)
    src_rect = src_img.get_rect()
    width = src_rect.width // cols
    height = src_rect.height // rows
    clip_rect = pygame.Rect(0, 0, width, height)
    ls = []
    for i in range(rows):
        for j in range(cols):
            clip_rect.x = j * width
            clip_rect.y = i * height
            ls.append(src_img.subsurface(clip_rect))
    return ls

#图片路径
img_dir = os.path.join(os.path.dirname(__file__), "imgs")

#游戏图标
IMAGE_GAMEICON = load_img_resources("Game_Icon.png")

#UI
IMAGE_PLAY_BK = load_img_resources("Background_Daytime.jpg")
IMAGE_CAEDFIELD = load_img_resources("ChooserBackground.png")
IMAGE_SHOVELSLOT = load_img_resources("ShovelSlot.png")
IMAGE_SHOVEL = load_img_resources("Shovel.png")
IMAGE_CARDS = [load_img_resources(f"Card_{plant}{i}.png") for plant in GAME_PLANT_BLOOD for i in range(2)]
IMAGE_LAWNCLEANER = load_img_resources("LawnCleaner.png")
IMAGE_FIAGEMETER_EMPTY = load_img_resources("FlagMeterEmpty.png"),\
                         load_img_resources("FlagMeterLevelProgress.png"),\
                         load_img_resources("FlagMeterFlag.png"),\
                         load_img_resources("FlagMeterZombieHead.png"),\
                         load_img_resources("FlagMeterFull.png")

#植物
IMAGE_SUNFLOWER = [load_img_resources(f"SunFlower{i}.png") for i in range(18)], [load_img_resources(f"SunFlower2{i}.png") for i in range(18)]
IMAGE_PEASHOOTER = [load_img_resources(f"PeaShooter{i}.png") for i in range(13)]
IMAGE_SNOWPEASHOOTER = [load_img_resources(f"SnowPeaShooter{i}.png") for i in range(15)]
IMAGE_REPEASHOOTER = [load_img_resources(f"RePeashooter{i}.png") for i in range(15)]
IMAGE_WALLNUT = [load_img_resources(f"WallNut{i}.png") for i in range(11)],\
                [load_img_resources(f"WallNut2{i}.png") for i in range(11)],\
                [load_img_resources(f"WallNut3{i}.png") for i in range(11)]
IMAGE_POTATOMINE =[load_img_resources("PotatoMine_notready.gif")],[load_img_resources(f"PotatoMine{i}.png") for i in range(8)]

#植物其他
IMAGE_SUN = [load_img_resources(f"Sun{i}.png") for i in range(22)]
IMAGE_PEABULLET = load_img_resources("PeaBullet.png")
IMAGE_PEABULLETHIT = load_img_resources("PeaBulletHit.png")
IMAGE_SNOWPEABULLET = load_img_resources("SnowPeaBullet.png")
IMAGE_GROWSOIL = [load_img_resources(f"GrowSoil{i}.png") for i in range(6)]
IMAGE_POTATOMINE_MASHED = load_img_resources("PotatoMine_mashed.gif")
IMAGE_POTATOMINE_BOOM = load_img_resources("PotatoMine_boom.gif")

#僵尸
IMAGE_ZOMBIE = [[[load_img_resources(f"Zombie{i}.png") for i in range(18)],[load_img_resources(f"ZombieLostHead{i}.png") for i in range(18)]],\
                [[load_img_resources(f"ZombieAttack{i}.png") for i in range(11)], [load_img_resources(f"ZombieLostHeadAttack{i}.png") for i in range(11)]]]
IMAGE_FLAGZOMBIE = [[[load_img_resources(f"FlagZombie{i}.png") for i in range(12)], [load_img_resources(f"FlagZombieLostHead{i}.png") for i in range(12)]],\
                    [[load_img_resources(f"FlagZombieAttack{i}.png") for i in range(11)], [load_img_resources(f"FlagZombieLostHeadAttack{i}.png") for i in range(11)]]]
IMAGE_CONEZOMBIE = [[[load_img_resources(f"ConeheadZombie{i}.png") for i in range(18)], [load_img_resources(f"ZombieLostHead{i}.png") for i in range(18)]],\
                    [[load_img_resources(f"ConeheadZombieAttack{i}.png") for i in range(11)], [load_img_resources(f"ZombieLostHeadAttack{i}.png") for i in range(11)]]]
IMAGE_BUCKETZOMBIE = [[[load_img_resources(f"BucketheadZombie{i}.png") for i in range(18)], [load_img_resources(f"ZombieLostHead{i}.png") for i in range(18)]],\
                      [[load_img_resources(f"BucketheadZombieAttack{i}.png") for i in range(11)], [load_img_resources(f"ZombieLostHeadAttack{i}.png") for i in range(11)]]]
IMAGE_LOSEHEAD = [load_img_resources(f"ZombieHead{i}.png") for i in range(12)]
IMAGE_ZOMBIEDIE = [load_img_resources(f"ZombieDie{i}.png") for i in range(10)]
IMAGE_ZOMBIEBOOMDIE = [load_img_resources(f"ZombieBoomDie{i}.png") for i in range(20)]
IMAGE_ZOMBIEBACK = [load_img_resources(f"ZombieBack{i}.png") for i in range(6)]

#其他
IMAGE_BUTTON = [load_img_resources(f"Button{i}.png") for i in range(2)]
IMAGE_ADVENTURE_BUTTON = split_image("SelectorScreenStartAdventure.png", 2, 1)
IMAGE_WAVE = [load_img_resources(f"Start{i}.png") for i in range(3)], load_img_resources("Middle.png"), load_img_resources("End.png")
IMAGE_LOSEGAME = load_img_resources("ZombiesWon.png")
IMAGE_PAUSE = [load_img_resources(f"dialog{i}.png") for i in range(10)]
IMAGE_LOAD = load_img_resources("PopCap_Logo.jpg")
IMAGE_TITLE = load_img_resources("TitleScreen.jpg")
IMAGE_PVZ = load_img_resources("PvZ_Logo.png")
IMAGE_LOADBAR_DIRT = load_img_resources("LoadBar_dirt.png"), load_img_resources("LoadBar_dirt.png")
IMAGE_LOADBAR_GRASS = load_img_resources("LoadBar_grass.png")
IMAGE_SODROLLCAP = load_img_resources("SodRollCap.png")
IMAGE_MAIN_BG = load_img_resources("main_bg.png")
IMAGE_ZOMBIENOTE = load_img_resources("ZombieNote.jpg")
IMAGE_VICTORY_GAME = load_img_resources("Credits_ZombieNote.png")

#音频路径
wav_dir = os.path.join(os.path.dirname(__file__), "wavs")
pygame.mixer.init() #初始化音频

#欢迎场景
WAV_LOADINGBAR_FLOW = load_wav_resources("loadingbar_flower.ogg")
WAV_LOADINGBAR_ZOMBIE = load_wav_resources("loadingbar_zombie.ogg")

#主界面场景
WAV_MAIN_BGM = load_wav_resources("lawnbgm.mp3")

#游戏场景
WAV_LAWNBGM_BATTLE = [load_wav_resources(f"lawnbgm_battle{i}.mp3") for i in range(3)]
WAV_READYGO = load_wav_resources("readysetplant.ogg")
WAV_AWOOGA = load_wav_resources("awooga.ogg")
WAV_WINMUSIC = load_wav_resources("winmusic.ogg")
WAV_LOSEMUSIC = load_wav_resources("losemusic.ogg")
WAV_SCREAM = load_wav_resources("scream.ogg")
WAV_LAWNMOWER = load_wav_resources("lawnmower.ogg")
WAV_GET_SUNLIGHT = load_wav_resources("points.ogg")
WAV_CHEECKD_CARD = load_wav_resources("checkd_card.ogg")
WAV_PLANT = [load_wav_resources(f"plant{i}.ogg") for i in range(2)]
WAV_IST_SHOVEL = load_wav_resources("tap.ogg")
WAV_IS_SHOVEL = load_wav_resources("shovel.ogg")
WAVE_FINALWAVE = load_wav_resources("finalwave.ogg")
WAVE_HUGEWAVE = load_wav_resources("hugewave.ogg")

#暂停场景
WAV_PAUSE = load_wav_resources("pause.ogg")

#按钮音效
WAV_WOODEN_BUTTONCLICK = load_wav_resources("buttonclick.ogg")
WAV_ROCKY_BUTTONCLICK = load_wav_resources("ceramic.ogg")

#植物音效
WAV_POTATO_BOOM = load_wav_resources("potato_mine.ogg")
WAV_DIRT_RISE = load_wav_resources("dirt_rise.ogg")

WAV_BUTTLE_BREAK = [load_wav_resources(f"splat{i}.ogg") for i in range(3)]
WAV_ZOMBIE_GROWL = [load_wav_resources(f"groan{i}.ogg") for i in range(6)]

#僵尸音效
WAV_EAT = [load_wav_resources(f"chomp{i}.ogg") for i in range(3)]
WAV_LOSE_HEAD = load_wav_resources("limbs_pop.ogg")
WAV_KILL_PLANT = load_wav_resources("gulp.ogg")
WAV_ZOMBIE_HAHAHA = load_wav_resources("evillaugh.ogg")

#未引用
