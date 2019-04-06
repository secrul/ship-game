import sys
import pygame
from settings import Settings
from bullet import Bullet
from alien import Alien
from time import sleep
from pygame.sprite import Sprite

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    #响应按键
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings,screen,ship)
            bullets.add(new_bullet)
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    #响应松开
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_events(ai_settings, screen,stats,play_button, ship,aliens, bullets):
    #响应按键和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
           check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_setting, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """玩家单击play按钮开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)

    if button_clicked and not stats.game_active:
        ai_setting.initialize_dynamic_setting()
        stats.reset_stats()
        stats.game_active = True
        pygame.mouse.set_visible(False)#隐藏光标

        #清空外星人类表和子弹列表
        aliens.empty()
        bullets.empty()

        #重新建立一批外星人，居中
        create_fleet(ai_setting,screen,ship,aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats,sb,ship, aliens, bullets,play_button):
    screen.fill(ai_settings.bg_color)
    sb.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    if not stats.game_active:
        play_button.draw_button()
    #让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, screen,stats,sb, ship, aliens, bullets):
    bullets.update()
    # 删除消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):#检测子弹和外星人的碰撞
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats,sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
def get_number_aliens_x(ai_settings, alien_width):
    avaliable_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(avaliable_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship,aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    #创建第一个外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
           create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_rows(ai_settings, ship_height, alien_height):

    avaliable_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(avaliable_space_y / (2 * alien_height))

    return number_rows
def update_aliens(ai_settings, stats,screen, ship, aliens, bullets):
    check_fleet_edgs(ai_settings, aliens)
    #检查飞船是否到达屏幕底部
    check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
        print("ship hit!!")

def check_fleet_edgs(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edgs():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """响应外星人撞到了飞船"""
    if stats.ship_left > 0:
        stats.ship_left -= 1
        aliens.empty()
        bullets.empty()
        #创建一批新的外星人,将飞船重新放在屏幕中间
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_setting, stats, screen, ship, aliens, bullets):
    """检查飞船是否到达屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #飞船撞到了屏幕底部
            ship_hit(ai_setting,stats,screen,ship,aliens,bullets)
            break

def check_high_score(stats,sb):
    """是不是产生最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()