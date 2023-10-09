import pygame
import random
import game_config
from game_config import GAME_KEYS, EVENT_GAME_OVER, WIDTH, HEIGHT
from game_resources import IMAGE_BUTTON, IMAGE_PAUSE, IMAGE_SUNFLOWER, IMAGE_LOAD, IMAGE_TITLE, IMAGE_PVZ, IMAGE_LOADBAR_DIRT, IMAGE_LOADBAR_GRASS, IMAGE_SODROLLCAP, IMAGE_MAIN_BG, IMAGE_ADVENTURE_BUTTON, \
                           WAV_LOADINGBAR_FLOW, WAV_LOADINGBAR_ZOMBIE, WAV_WOODEN_BUTTONCLICK, WAV_ROCKY_BUTTONCLICK, WAV_PAUSE, WAV_LOSEMUSIC, WAV_MAIN_BGM, WAV_LAWNBGM_BATTLE, WAV_WINMUSIC, WAV_SCREAM, WAV_EAT, WAV_ZOMBIE_HAHAHA
from game_condition import Game_Victory, Game_Defeated

#场景父类
class _Scene:                               #规范接口
    def draw(self, frane):pass
    def update(self, frame):pass
    def handle_event(self, frame):pass

#加载场景--子类
class _Load_Scene(_Scene):
    def __init__(self):
        self.alpha = 0
        self.speed = 6

    def draw(self, frame):
        frame.canvas.fill((0,0,0))
        img = IMAGE_LOAD.convert_alpha()
        img.set_alpha(self.alpha)
        rect_frame = frame.canvas.get_rect()
        rect_image = img.get_rect(center = rect_frame.center)
        frame.canvas.blit(img, rect_image)

    def update(self, frame): 
        self.alpha += self.speed
        if self.alpha >= 400:
            self.speed = -4

    def handle_event(self, frame):
        if self.alpha < 0:
            frame.activate_scene = welcom_scene

#欢迎场景--子类
#(按钮升起动画)
class _Welcome_Scene(_Scene):
    def __init__(self):
        self.img = IMAGE_TITLE
        self.sodrollcap = IMAGE_SODROLLCAP.copy()
        self.sodrollcap_rect = self.sodrollcap.get_rect()
        self.grass = IMAGE_LOADBAR_GRASS
        self.dirt = IMAGE_LOADBAR_DIRT[0]

        self.btn_sur = pygame.surface.Surface((314, 71))
        pygame.Surface.set_colorkey(self.btn_sur, "black")

        self.buttons = []
        self.btn_toplef = (self.img.get_width() - IMAGE_LOADBAR_DIRT[0].get_width()) / 2, self.img.get_height() - IMAGE_LOADBAR_DIRT[0].get_height() - 13
        btn_center = self.img.get_width() / 2, self.img.get_height() - 13 - IMAGE_LOADBAR_DIRT[0].get_height() / 2
        btn_start = Button(IMAGE_LOADBAR_DIRT, (btn_center), "Click Start", 30)
        btn_start.on_click = self.btn_start_lick
        self.buttons.append(btn_start)

        self.move_speed = 2
        self.pvz_move = 0
        self.grass_move = 0

        self.sodrollcap_factor = 1
        self.rotate_speed = 4.5
        self.rotate_angle = 0

        self.sound_num = 0

    def sound_effect(self):
        sound_time = [50, 100, 150, 200, 250]
        if self.sound_num < 5 and self.grass_move >= sound_time[self.sound_num]:
            WAV_LOADINGBAR_FLOW.play()
            self.sound_num += 1
        if self.sound_num == 5:
            WAV_LOADINGBAR_ZOMBIE.play()
            self.sound_num += 1

    def btn_start_lick(self, frame):
        WAV_WOODEN_BUTTONCLICK.play()
        WAV_MAIN_BGM.play(-1)
        frame.activate_scene = start_scene

    def draw(self, frame):
        image = self.img.copy()
        image.blit(IMAGE_PVZ, ((image.get_width() - IMAGE_PVZ.get_width()) / 2, -IMAGE_PVZ.get_height() + self.pvz_move))
        self.sodrollcap = pygame.transform.scale(IMAGE_SODROLLCAP, (int(IMAGE_SODROLLCAP.get_width() * self.sodrollcap_factor), int(IMAGE_SODROLLCAP.get_height() * self.sodrollcap_factor)))
        self.sodrollcap = pygame.transform.rotate(self.sodrollcap, self.rotate_angle)
        self.sodrollcap_rect = self.sodrollcap.get_rect(center = self.sodrollcap_rect.center)
        self.sodrollcap_rect.centerx += self.move_speed

        self.btn_sur.fill((0,0,0))
        self.btn_sur.blit(self.grass, (-self.grass.get_width() + self.grass_move, 38))
        self.btn_sur.blit(self.sodrollcap, (self.sodrollcap_rect.left - 50, self.sodrollcap_rect.top + 7)) if self.grass_move <= self.btn_sur.get_width()-7 else None

        rect_frame = frame.canvas.get_rect()
        rect_image = image.get_rect(center = rect_frame.center)
        frame.canvas.blit(image, rect_image)

        for buttion in self.buttons:
            buttion.draw(frame.canvas)
        frame.canvas.blit(self.btn_sur, (self.btn_toplef[0]+3, self.btn_toplef[1] - 53))

    def update(self, frame):
        self.sound_effect()
        if self.grass_move <= self.btn_sur.get_width()-7:
            self.grass_move += self.move_speed
            self.sodrollcap_factor -= (33 / IMAGE_SODROLLCAP.get_width()) / self.btn_sur.get_width() * self.move_speed
            self.rotate_angle -= self.rotate_speed
        if self.pvz_move < IMAGE_PVZ.get_height() + 14:
            self.pvz_move += self.move_speed
        self.grass_move += 0
        self.pvz_move += 0

    def handle_event(self, frame):
        es = pygame.event.get()
        for btn in self.buttons:
            btn.handle_event(frame, es)

#主场景--子类
#(帮助、退出)
class _Start_Scene(_Scene):
    def __init__(self):
        self.buttons = []
        btn_pos = 545, 135
        btn_adventure_begins = Button(IMAGE_ADVENTURE_BUTTON, (btn_pos), transform = 1.1)
        btn_adventure_begins.on_click = self.btn_adventure_begins_lick
        self.buttons.append(btn_adventure_begins)

        self.game_bgm = None

    def btn_adventure_begins_lick(self, frame):
        # sound = WAV_LOSEMUSIC.play()
        # sound.queue(WAV_ZOMBIE_HAHAHA)
        WAV_ROCKY_BUTTONCLICK.play()
        WAV_MAIN_BGM.stop()
        # self.game_bgm = random.choice(WAV_LAWNBGM_BATTLE).play()
        frame.server.start()
        frame.activate_scene = play_scene

    def draw(self, frame):
        image = IMAGE_MAIN_BG
        rect_image = image.get_rect(topleft = (-100, 0))
        frame.canvas.blit(image, rect_image)

        for buttion in self.buttons:
            buttion.draw(frame.canvas)

    def handle_event(self, frame):
        es = pygame.event.get()
        for btn in self.buttons:
            btn.handle_event(frame, es)

#游玩场景--子类
class _Play_Scene(_Scene):
    def draw(self, frame):
        frame.server.draw(frame.canvas)

    def update(self, frame): 
        frame.server.update()

    def handle_event(self, frame):
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == GAME_KEYS["pause"]:
                # start_scene.game_bgm.stop()
                WAV_PAUSE.play()
                frame.activate_scene = pause_scene
                return
            if e.type == EVENT_GAME_OVER:
                if e.state:
                    # start_scene.game_bgm.stop()
                    WAV_WINMUSIC.play()
                    frame.activate_scene = victory_scene
                    return
                else:
                    # start_scene.game_bgm.stop()
                    sound = WAV_LOSEMUSIC.play()
                    sound.queue(random.choice(WAV_EAT))
                    sound.queue(WAV_SCREAM)
                    
                    frame.activate_scene = defeated_scene
                    return
            pygame.event.post(e)
        frame.server.handle_event()

#暂停场景--子类
class _Pause_Scene(_Scene):
    def __init__(self):
        self.pause_image, self.size = self.join_pause_image()
        pause_topleft = (WIDTH - self.size[0]) / 2, (HEIGHT- self.size[1]) / 2

        self.fps = 5
        self.image_index = 0
        self.sunflower_image = IMAGE_SUNFLOWER[0][self.image_index]
        self.sunflower_pos = (self.size[0]-self.sunflower_image.get_width())/2, (self.size[1]-self.sunflower_image.get_height())/2-15

        self.buttons = []
        btn_pos = pause_topleft[0] + self.size[0] / 2, pause_topleft[1] + 310
        btn_back_game = Button(IMAGE_BUTTON, (btn_pos), "back to game", 40, 0.8)
        btn_back_game.on_click = self.btn_back_game_lick
        self.buttons.append(btn_back_game)

    def join_pause_image(self):
        factor = 1.253125
        pause_images = []
        for i in range(len(IMAGE_PAUSE)):
            pause_images.append(pygame.transform.scale(IMAGE_PAUSE[i], (int(IMAGE_PAUSE[i].get_size()[0] * factor), int(IMAGE_PAUSE[i].get_size()[1] * factor))))
        
        image_header = pause_images[0]       #234/80
        image_topleft = pause_images[1]      #134/121
        image_topmiddle = pause_images[2]    #116/121
        image_topright = pause_images[3]     #150/121
        image_centerleft = pause_images[4]   #134/67
        image_centermiddle = pause_images[5] #116/67
        image_centerright = pause_images[6]  #131/67
        image_bottomleft =  pause_images[7]  #134/121
        image_bottommiddle = pause_images[8] #116/121
        image_bottomright = pause_images[9]  #135/121

        size = image_topleft.get_width() + image_topmiddle.get_width() + image_topright.get_width(),\
               image_header.get_height() + image_topleft.get_height() + image_centerleft.get_height() + image_bottomleft.get_height()
        pause_image = pygame.Surface(size)
        pygame.Surface.set_colorkey(pause_image, "black")
        
        head = (size[0]-image_header.get_width())/2, 0
        col_1 = 0
        col_2 = col_1 + image_topleft.get_width()
        col_3 = col_2 + image_topmiddle.get_width()
        row_1 = image_header.get_height() - 24            #头图片底部有24像素的偏差
        row_2 = row_1 + image_topleft.get_height()
        row_3 = row_2 + image_centerleft.get_height()
        
        pause_image.blit(image_topleft,(col_1, row_1))
        pause_image.blit(image_topmiddle,(col_2, row_1))
        pause_image.blit(image_topright,(col_3, row_1))
        pause_image.blit(image_centerleft,(col_1, row_2))
        pause_image.blit(image_centermiddle,(col_2, row_2))
        pause_image.blit(image_centerright,(col_3, row_2))
        pause_image.blit(image_bottomleft,(col_1, row_3))
        pause_image.blit(image_bottommiddle,(col_2, row_3))
        pause_image.blit(image_bottomright,(col_3, row_3))
        pause_image.blit(image_header, (head))

        font_1 = pygame.font.Font(None, 36)
        font_2 = pygame.font.Font(None, 30)
        font_image_1 = font_1.render("Game Pause", True, "orange")
        font_pos_1 = ((size[0] - font_image_1.get_width()) / 2, 100)
        font_image_2 = font_2.render("click back to game", True, "orange")
        font_pos_2 = ((size[0] - font_image_2.get_width()) / 2, 230)
        pause_image.blit(font_image_1, font_pos_1)
        pause_image.blit(font_image_2, font_pos_2)

        return pause_image, size

    def btn_back_game_lick(self, frame):
        WAV_WOODEN_BUTTONCLICK.play()
        frame.activate_scene = play_scene

    def draw(self, frame):
        if game_config.FRAMECOUNT % self.fps == 0:
            self.image_index = (self.image_index + 1) % len(IMAGE_SUNFLOWER[0])
        self.sunflower_image = IMAGE_SUNFLOWER[0][self.image_index]
        self.pause_image = self.join_pause_image()[0]
        self.pause_image.blit(self.sunflower_image, (self.sunflower_pos))

        rect_frame = frame.canvas.get_rect()
        rect_image = self.pause_image.get_rect(center = rect_frame.center)
        frame.canvas.blit(self.pause_image, rect_image)

        for buttion in self.buttons:
            buttion.draw(frame.canvas)

    def handle_event(self, frame):
        for e in pygame.event.get(pygame.KEYDOWN):
            if e.key == GAME_KEYS['pause']:
                frame.activate_scene = play_scene
        es = pygame.event.get()
        for btn in self.buttons:
            btn.handle_event(frame, es)

#获胜场景--子类
class _Victory_Scene(_Scene):
    def __init__(self):
        self.animation = Game_Victory()

    def draw(self, frame):
        frame.server.draw(frame.canvas)
        self.animation.draw(frame.canvas)
        
    def update(self, frame):
        self.animation.update()
        
    def handle_event(self, frame):
        for e in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            WAV_WOODEN_BUTTONCLICK.play()
            WAV_MAIN_BGM.play(-1)
            frame.activate_scene = start_scene

#失败场景--子类
class _Defeated_Scene(_Scene):
    def __init__(self):
        self.animation = Game_Defeated()

    def draw(self, frame):
        frame.server.draw(frame.canvas)
        self.animation.draw(frame.canvas)
        
    def update(self, frame):
        self.animation.update()
        
    def handle_event(self, frame):
        for e in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            WAV_WOODEN_BUTTONCLICK.play()
            WAV_MAIN_BGM.play(-1)
            frame.activate_scene = start_scene

#按钮类
#(添加反馈--鼠标移动到按钮区域，文字变红)
class Button(pygame.sprite.Sprite):
    def __init__(self, button_img, center, write = None, write_size = 0, transform = 1):
        img = button_img[0]
        btn_width = int(img.get_width() * transform)
        btn_height = int(img.get_height() * transform)
        self.botton_1 = pygame.transform.scale(button_img[0], (btn_width, btn_height))
        self.botton_2 = pygame.transform.scale(button_img[1], (btn_width, btn_height))
        self.font = pygame.font.SysFont("time new roman", write_size, True)

        self.image = self.botton_1
        self.rect = self.image.get_rect(center = center)
        self.write = write
        self.write_center = btn_width/2, btn_height/2

        self.is_selected = False
        self.not_selected_botton()

    def not_selected_botton(self):
        if self.write:
            write = self.font.render(self.write, True, "green")
            write_pos = self.write_center[0] - write.get_size()[0]/2, self.write_center[1] - write.get_size()[1]/2
            self.image = self.botton_1.copy()
            self.image.blit(write, write_pos)
        else:
            self.image = self.botton_1

    def is_selected_botton(self):
        if self.write:
            write = self.font.render(self.write, True, "red")
            write_pos = self.write_center[0] - write.get_size()[0]/2, self.write_center[1] - write.get_size()[1]/2
            self.image = self.botton_2.copy()
            self.image.blit(write, write_pos)
        else:
            self.image = self.botton_2

    def draw(self, surf):
        if self.is_selected:self.is_selected_botton()
        else:self.not_selected_botton()
        surf.blit(self.image, self.rect)
        
    def handle_event(self, frame, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                self.is_selected = self.rect.collidepoint(e.pos)
            if self.is_selected and e.type == pygame.MOUSEBUTTONUP:
                self.on_click(frame)
                self.is_selected = False

    def on_click(self, frame):
        pass

load_scene = _Load_Scene()
welcom_scene = _Welcome_Scene()
start_scene = _Start_Scene()
play_scene = _Play_Scene()
pause_scene = _Pause_Scene()
victory_scene = _Victory_Scene()
defeated_scene = _Defeated_Scene()

#374