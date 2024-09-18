import pygame
import os
import config.screen as conf_screen
import config.colors as colors
import entities.player as player_config
import terrain.Platformer as terPlatform
import season_cycle as season_cycle_manager
import pytmx

pygame.init()

screen = pygame.display.set_mode((conf_screen.WIDTH_SCREEN, conf_screen.HEIGHT_SCREEN))
grid = [[0 for x in range(conf_screen.COLS)] for y in range(conf_screen.ROWS)]

season_cycle = season_cycle_manager.SeasonCycle(screen, conf_screen.CELL_SIZE*2, conf_screen.CELL_SIZE*2, conf_screen.CELL_SIZE*.2, conf_screen.CELL_SIZE*.2)

tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
SCALE_FACTOR = 2

pygame.display.set_caption("Seasonal Odyssey")

GRAVITE = 0.8
PATH = os.path.dirname(__file__)

sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

player = player_config.Player()
sprites.add(player)

for layer in tmx_data.visible_layers:
    if isinstance(layer, pytmx.TiledObjectGroup):
        if layer.name == "collision_layer":
            for obj in layer:
                # Crée un rectangle pour chaque objet de collision
                rect = pygame.Rect(obj.x* SCALE_FACTOR, obj.y* SCALE_FACTOR, obj.width* SCALE_FACTOR, obj.height* SCALE_FACTOR)
                platform = terPlatform.Platform(rect.width, rect.height, rect.x, rect.y)
                if (platform.enable_collision):
                    platforms.add(platform)
                    sprites.add(platform)

def draw_specific_layers(layers_to_draw):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            if layer.name in layers_to_draw:  # Vérifie si le layer est dans la liste à dessiner
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        # Applique le scaling à la tuile
                        scaled_tile = pygame.transform.scale(tile, (tmx_data.tilewidth * SCALE_FACTOR, tmx_data.tileheight * SCALE_FACTOR))
                        
                        # Affiche la tuile à la position correcte avec le scaling appliqué
                        screen.blit(scaled_tile, (x * tmx_data.tilewidth * SCALE_FACTOR, y * tmx_data.tileheight * SCALE_FACTOR))

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
    player.update()
    
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
    
    # Mettre à jour et afficher le cycle des saisons
    season_cycle.update_needle_rotation()
    season_cycle.show_season_cycle()

    # Afficher la saison actuelle
    current_season = season_cycle.current_season()

    if current_season in ['Spring', 'Autumn']:
        draw_specific_layers(season_cycle.SEASON_LAYERS[current_season])

    pygame.display.flip()

    season_cycle.elapsed_time = pygame.time.get_ticks() // (1000//8)
    clock.tick(60)

pygame.quit()
