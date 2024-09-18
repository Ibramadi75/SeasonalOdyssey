import pygame
import os
import config.screen as conf_screen
import config.colors as colors
import entities.player as player_config
import terrain.Platformer as terPlatform

pygame.init()

screen = pygame.display.set_mode((conf_screen.WIDTH_SCREEN, conf_screen.HEIGHT_SCREEN))
grid = [[0 for x in range(conf_screen.COLS)] for y in range(conf_screen.ROWS)]

pygame.display.set_caption("Seasonal Odyssey")

GRAVITE = 0.8
PATH = os.path.dirname(__file__)

sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

player = player_config.Player()
sprites.add(player)

platform = terPlatform.Platform(conf_screen.WIDTH_SCREEN, 20, 0, conf_screen.HEIGHT_SCREEN - 100)
if (platform.enable_collision):
    platforms.add(platform)

sprites.add(platform)

clock = pygame.time.Clock()
isRunning = True

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_RIGHT:
                player.move_right()
            if event.key == pygame.K_LEFT:
                player.move_left()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player.stop()
                
    sprites.update()

    if not player.is_grounded:
        player.gravite()
        
    player.rect.x += player.x_current_speed
    player.rect.y += player.y_current_speed
    
    if player.rect.right >conf_screen.WIDTH_SCREEN:
        player.rect.right = conf_screen.WIDTH_SCREEN
    if player.rect.left < 0:
        player.rect.left = 0

    if player.rect.bottom > conf_screen.HEIGHT_SCREEN:
        player.rect.bottom = conf_screen.HEIGHT_SCREEN
        player.is_grounded = True
        player.y_current_speed = 0
    
    collided_platform = pygame.sprite.spritecollide(player, platforms, False)
    if collided_platform:
        player.rect.bottom = collided_platform[0].rect.top
        player.is_grounded = True
        player.y_current_speed = 0
    else:
        player.is_grounded = False

    screen.fill(colors.WHITE)
    conf_screen.draw_grid(grid, screen)
    sprites.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
