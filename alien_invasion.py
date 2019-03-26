import pygame
from settings import  Settings
from ship import  Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStates
from button import Button
from scoreboard import Scoreboard

def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display. set_mode((ai_settings.screen_width, ai_settings.screen_height))
    ship = Ship(ai_settings, screen)
    pygame.display.set_caption("Alien Invasion")
    stats = GameStates(ai_settings)
    # 创建一个用于存储子弹的编组
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, aliens, ship)
    play_button = Button(screen, "Play!")
    scoreboard = Scoreboard(screen, stats, ai_settings)
    # 开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(scoreboard, ai_settings, screen, ship, bullets, play_button, stats, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(stats, scoreboard, ai_settings, bullets, aliens, screen, ship)
            gf.update_aliens(scoreboard, ai_settings, ship, aliens, stats, bullets, screen)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets, play_button, stats, scoreboard)

run_game()
