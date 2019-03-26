import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(scoreboard, ai_settings, screen, ship, buttles, play_button, stats, aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings, screen, ship,buttles)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_play_button(scoreboard, ai_settings, screen, play_button, stats, aliens, ship, bullets)

def update_screen(ai_settings, screen, ship, aliens, buttles, play_button, stats, scoreboard):
    screen.fill(ai_settings.bg_color)
    scoreboard.show_score()
    # 每次循环时都重绘屏幕
    for buttle in buttles.sprites():
        buttle.draw_buttle()

    ship.blitme()
    aliens.draw(screen)
    if not stats.game_active:
        play_button.draw_button()
    # 让最近的屏幕可见
    pygame.display.flip()

def check_keydown_events(event,ai_settings, screen, ship, bullets):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        if event.key == pygame.K_LEFT:
            ship.moving_left = True
        if event.key == pygame.K_SPACE:
            fire_buttle(ai_settings, screen, ship, bullets)

def check_keyup_events(event, ship):
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        if event.key == pygame.K_LEFT:
            ship.moving_left = False

def update_bullets(stats, scoreboard, ai_settings, bullets, aliens, screen, ship):
    bullets.update()
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        stats.score += ai_settings.alien_point
        scoreboard.prep_score()
        check_high_score(stats, scoreboard)
    if len(aliens) == 0:
        bullets.empty()
        stats.level += 1
        scoreboard.prep_level()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, aliens, ship)
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)

def fire_buttle(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullet_allowed:
        new_buttle = Bullet(ai_settings, screen, ship)
        bullets.add(new_buttle)

def create_fleet(ai_settings, screen, aliens, ship):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings,ship, alien)
    for number_row in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, aliens ,screen, alien_number, number_row)

def get_number_aliens_x(ai_settings, alien_width):

    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return int(number_aliens_x)

def create_alien(ai_settings, aliens, screen,alien_number, number_row):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + alien_width * alien_number * 2
    alien.rect.x = alien.x
    alien.rect.y = number_row * alien.rect.height + alien.rect.height
    aliens.add(alien)

def get_number_rows(ai_settings, ship, alien):
    available_space_x = ai_settings.screen_height/2 - ship.rect.height
    number_rows = available_space_x/alien.rect.height
    return int(number_rows)

def update_aliens(scoreboard, ai_settings, ship, aliens, stats, bullets, screen):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    check_aliens_bottom(stats, aliens, screen, bullets, ai_settings, ship)
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(scoreboard, stats, aliens, bullets, ai_settings, screen, ship)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(scoreboard, stats, aliens, bullets, ai_settings, screen, ship):
    if stats.ship_left > 0:
        stats.ship_left -= 1
        scoreboard.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(stats, aliens, screen, bullets, ai_settings, ship):
    for alien in aliens.sprites():
        if alien.rect.y >= ai_settings.screen_height:
            ship_hit(stats, aliens, bullets, ai_settings, screen, ship)

def check_play_button(scoreboard, ai_settings, screen, play_button, stats, aliens, ship, bullets):
    if play_button.rect.collidepoint(pygame.mouse.get_pos())and not stats.game_active:
        ai_settings.initialize_settings()
        stats.game_active = True
        stats.reset_stats()
        scoreboard.prep_score()
        scoreboard.prep_level()
        scoreboard.prep_ships()
        aliens.empty()
        bullets.empty()
        ship.center_ship()
        create_fleet(ai_settings, screen, aliens, ship)
        pygame.mouse.set_visible(False)

def check_high_score(stats, scoreboard):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()