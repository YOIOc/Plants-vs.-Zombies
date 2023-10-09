import sys
import pygame
import game_config
from game_config import WIDTH, HEIGHT, GAMEFPS, GAMETITLE
from game_resources import IMAGE_GAMEICON
from game_scene import load_scene
from game_server import GameServer

#游戏主程序
class MainFrame:
    def __init__(self):
        pygame.display.set_caption(GAMETITLE)                       #设置窗口标题
        pygame.display.set_icon(IMAGE_GAMEICON)                     #设置窗口图标
        self.canvas = pygame.display.set_mode((WIDTH, HEIGHT))      #创建窗口
        self.clock = pygame.time.Clock()                            #创建时钟对象

        self.server = GameServer()                                  #创建游戏服务器对象
        self.activate_scene = load_scene                            #激活场景

    #游戏主循环
    def main_loop(self):
        while True:
            game_config.FRAMECOUNT += 1
            self.clock.tick(GAMEFPS)
            self.check_for_quit()
            self.activate_scene.handle_event(self)
            self.activate_scene.update(self)
            self.activate_scene.draw(self)
            pygame.display.flip()

    def check_for_quit(self):
        for e in pygame.event.get(pygame.QUIT):
            self.terminate()
        for e in pygame.event.get(pygame.KEYDOWN): #括号中若传入参数(事件类型)，那么只获取并删除指定类型的事件
            if e.key == pygame.K_ESCAPE:
                self.terminate()
            pygame.event.post(e)                   #将事件重新放入事件队列中

    def terminate(self):                           #退出游戏
        pygame.quit()
        sys.exit()

#41