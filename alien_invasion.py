import pygame
from ship import Ship
from settings import Settings
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from Button import Button
from scoreboad import Scoreboard

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('alien invasion')
    play_button = Button(ai_settings,screen,"Begin")
    stats = GameStats(ai_settings)
    bg_color = (0,255,255)
    sb = Scoreboard(ai_settings,screen,stats)
    #创建船
    ship = Ship(ai_settings,screen)
    #创建储存子弹的数组
    bullets = Group()
    aliens = Group()
    alien = Alien(ai_settings, screen)

    #创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    while True:
        gf.check_events(ai_settings, screen,stats,play_button, ship,aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen,stats,sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats,screen,ship, aliens,bullets)

        bullets.update()
        gf.update_screen(ai_settings, screen, stats,sb,ship, aliens, bullets,play_button)


        #删除消失的子弹
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)


run_game()