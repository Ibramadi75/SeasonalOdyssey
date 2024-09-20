import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import config.screen as conf_screen
import config.colors as colors
import entities.player as player_config
from menu import show_pause_menu, show_start_menu
import terrain.Platformer as platformer
import season_cycle as season_cycle_manager
import pytmx

pygame.mixer.init()

# Load the music file
music_path = 'music/sound_theme2.mp3'
if os.path.exists(music_path):
    pygame.mixer.music.load(music_path)
else:
    print("Music file not found!")

pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((conf_screen.WIDTH_SCREEN, conf_screen.HEIGHT_SCREEN))

grid = [[0 for x in range(conf_screen.COLS)] for y in range(conf_screen.ROWS)]

season_cycle = season_cycle_manager.SeasonCycle(screen, conf_screen.CELL_SIZE*4, conf_screen.CELL_SIZE*4, conf_screen.CELL_SIZE*.2, conf_screen.CELL_SIZE*.2)

tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
SCALE_FACTOR = 2

pygame.display.set_caption("Seasonal Odyssey")

GRAVITE = 0.8
SCROLL_SPEED = 1
SCROLL_THRESHOLD = 0.25 * conf_screen.WIDTH_SCREEN 


PATH = os.path.dirname(__file__)

# Charger l'image
background_image = pygame.image.load('assets/winter/background/background.png').convert()
background_image = pygame.transform.scale(background_image, (conf_screen.WIDTH_SCREEN, conf_screen.HEIGHT_SCREEN))

day_duration_ms = 100  # 0.1 seconds for 1 in-game day
added_time_ms = 0      # Additional time in milliseconds

sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
platforms_lava = pygame.sprite.Group()

player = player_config.Player(platforms)
sprites.add(player)

for layer in tmx_data.visible_layers:
    if isinstance(layer, pytmx.TiledObjectGroup):
        if layer.name == "collision_layer":
            for obj in layer:
                # Crée un rectangle pour chaque objet de collision
                rect = pygame.Rect(obj.x* SCALE_FACTOR, obj.y* SCALE_FACTOR, obj.width* SCALE_FACTOR, obj.height* SCALE_FACTOR)
                platform = platformer.Platform(rect.width, rect.height, rect.x, rect.y)
                surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                platform.image = surface
                platforms.add(platform)

        if layer.name == "lava_collision_layer":
            for obj in layer:
                # Crée un rectangle pour chaque objet de collision
                rect = pygame.Rect(obj.x* SCALE_FACTOR, obj.y* SCALE_FACTOR, obj.width* SCALE_FACTOR, obj.height* SCALE_FACTOR)
                platform = platformer.Platform(rect.width, rect.height, rect.x, rect.y)
                surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                platform.image = surface
                platforms_lava.add(platform)

        if layer.name == "gem_collision_layer":
            for obj in layer:
                # Crée un rectangle pour chaque objet de collision
                rect = pygame.Rect(obj.x* SCALE_FACTOR, obj.y* SCALE_FACTOR, obj.width* SCALE_FACTOR, obj.height* SCALE_FACTOR)
                platform = platformer.Platform(rect.width, rect.height, rect.x, rect.y)
                surface = pygame.Surface((rect.width, rect.height))
                platform.image = surface
                gem = platform  # Assigner cette plateforme à l'objet "gemme"


# Fonction pour dessiner les couches spécifiques en tenant compte du défilement horizontal
def draw_visible_tiles(layers_to_draw, scroll_x):
    # Taille d'une tuile
    tile_width = tmx_data.tilewidth * SCALE_FACTOR
    tile_height = tmx_data.tileheight * SCALE_FACTOR

    # Taille de l'écran en nombre de tuiles
    tiles_in_screen_width = conf_screen.WIDTH_SCREEN // tile_width + 1
    tiles_in_screen_height = conf_screen.HEIGHT_SCREEN // tile_height

    # Position du joueur dans la grille des tuiles
    start_x = scroll_x // tile_width
    start_y = 0  # Si on veut un scrolling uniquement horizontal

    # Offset de la caméra
    offset_x = scroll_x % tile_width

    # Parcourir les couches spécifiées
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer) and layer.name in layers_to_draw:
            # Utiliser la méthode layer.tiles() pour obtenir les tuiles (x, y, tile)
            for x, y, tile in layer.tiles():
                if tile:  # S'assurer que la tuile existe
                    # Vérifie si la tuile est visible à l'écran
                    if start_x <= x < start_x + tiles_in_screen_width:
                        # Applique le scaling à la tuile
                        scaled_tile = pygame.transform.scale(tile, (tile_width, tile_height))

                        # Calculer la position où dessiner la tuile à l'écran en fonction du scrolling
                        screen_x = (x - start_x) * tile_width - offset_x
                        screen_y = y * tile_height

                        # Dessiner la tuile à la position calculée
                        screen.blit(scaled_tile, (screen_x, screen_y))

def add_sprites_to_group(layer_string_list, group):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledObjectGroup):
            if layer.name in layer_string_list:
                for obj in layer:
                    # Crée un rectangle pour chaque objet de collision
                    rect = pygame.Rect(
                        (obj.x * SCALE_FACTOR) - scroll_x_camera,  # Appliquer le décalage de la caméra sur l'axe X
                        obj.y * SCALE_FACTOR, 
                        obj.width * SCALE_FACTOR, 
                        obj.height * SCALE_FACTOR
                    )
                    platform = platformer.Platform(rect.width, rect.height, rect.x, rect.y, layer.name)
                    group.add(platform)

    return group

def remove_sprites_to_group(layer, group):
    for platform in group:
        if platform.id == layer:
            group.remove(platform)
            sprites.remove(platform)

    return group

def remove_all_but_one_group(group, group_to_keep):
    for platform in group:
        if platform.id != group_to_keep:
            group.remove(platform)

    return group

def get_time_string(elapsed_time_ms):
    # Convertir ce temps en secondes
    elapsed_seconds = elapsed_time_ms // 1000

    # Calculer les heures, minutes et secondes
    hours = elapsed_seconds // 3600
    minutes = (elapsed_seconds % 3600) // 60
    seconds = elapsed_seconds % 60

    # Formater le temps en "hh:mm:ss"
    time_string = f"{hours:02}h:{minutes:02}m:{seconds:02}s"

    return time_string


scroll_x_camera = 0
scroll_x = 0

clock = pygame.time.Clock()
isRunning = True

inPause = False
isFinish = False

image = pygame.image.load('assets/UI/menu/end_screen.jpg')

is_menu_displayed = show_start_menu(screen)
time_to_sub = pygame.time.get_ticks()

while isRunning:
    scroll_x = 0
    actual_platforms = remove_all_but_one_group(platforms, "terrain")
    sprites = remove_all_but_one_group(sprites, "terrain")
    if is_menu_displayed == "play":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player.stop()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] :
            player.move_left()
        if keys[pygame.K_RIGHT] :
            player.move_right()
        if keys[pygame.K_SPACE] :
            player.jump()
        if keys[pygame.K_t]:
            added_time_ms  += day_duration_ms // 32
        if keys[pygame.K_ESCAPE]:
            # Afficher le menu de pause
            if show_pause_menu(screen) == False:
                continue  # Reprendre le jeu
            
        if is_menu_displayed == True:
            is_menu_displayed = show_pause_menu(screen)

        # Ne faire défiler la caméra que si le joueur avance (vitesse positive)
        if player.x_current_speed > 0 and player.rect.right > SCROLL_THRESHOLD:
            scroll_x_camera += player.def_move_speed * SCROLL_SPEED  # La caméra défile seulement vers la droite
            scroll_x = player.def_move_speed * SCROLL_SPEED
            player.move_speed = 1
        else :
            player.move_speed = player.def_move_speed

        # Ici on fait défiler toutes les plateformes
        platforms.update(scroll_x)
        platforms_lava.update(scroll_x)

        # Le joueur ne peut pas sortir de l'écran à gauche (limite de la fenêtre du début)
        if player.rect.left < 0:
            player.rect.left = 0

        collided_lava = pygame.sprite.spritecollide(player, platforms_lava, False)
        # Si le joueur tombe sous l'écran, il meurt et le jeu recommence au TOUT début en remontant meme le background et remettant le joueur en position initiale
        if player.rect.top > conf_screen.HEIGHT_SCREEN or collided_lava:
            player.rect.x = 200
            player.rect.y = 100
            player.is_grounded = False
            player.y_current_speed = 0
            player.x_current_speed = 0
            player.started_age += 3

        screen.blit(background_image, (0, 0))
        
        #conf_screen.draw_grid(grid, screen)
        season_cycle.elapsed_time = (pygame.time.get_ticks() // (day_duration_ms)) + (added_time_ms)
        
        
        # Mettre à jour et afficher le cycle des saisons
        if not isFinish:
            season_cycle.update_needle_rotation()
            season_cycle.show_season_cycle()
            
            player.update_age(season_cycle.year_elapsed())

        current_season = season_cycle.current_season()

        if current_season == "Spring":
            draw_visible_tiles(["water_layer", "lava_layer", "tree1_layer"], scroll_x_camera)
            actual_platforms = add_sprites_to_group(["collision_tree1_layer"], actual_platforms)
        elif current_season == "Summer":
            draw_visible_tiles(["lava_layer", "tree2_layer"], scroll_x_camera)
            actual_platforms = add_sprites_to_group(["collision_tree2_layer"], actual_platforms)
        elif current_season == "Autumn":
            draw_visible_tiles(["water_layer", "lava_layer", "lava_block_partial_layer", "tree3_layer"], scroll_x_camera)
            actual_platforms = add_sprites_to_group(["collision_tree3_layer", "lava_partial_collision_layer"], actual_platforms)
        elif current_season == "Winter":
            draw_visible_tiles(["ice_layer", "lava_block_layer", "tree0_layer"], scroll_x_camera)
            actual_platforms = add_sprites_to_group(["collision_tree0_layer", "ice_collision_layer", "lava_block_collision_layer"], actual_platforms)

        draw_visible_tiles([season_cycle.SEASON_LAYERS[current_season], "decorations_layer"], scroll_x_camera)
        sprites.draw(screen)

        player.show_age(screen)
        player.is_jumping = False

        player.update(actual_platforms)

        collided_platform = pygame.sprite.spritecollide(player, actual_platforms, False)
        if collided_platform:
            player.is_grounded = True
            player.y_current_speed = 0
            player.rect.bottom = collided_platform[0].rect.top

        elif not collided_platform:
            player.is_grounded = False

        if not isFinish:
            font_time = pygame.font.Font(None, 36)
            text_time = get_time_string(pygame.time.get_ticks() - time_to_sub)
            padding = 50
            text_time_render = font_time.render(text_time, True, colors.BLACK)
            screen.blit(text_time_render, (conf_screen.WIDTH_SCREEN // 2 - padding, padding))

        # detect end game
        if gem:
            gem.rect.x -= scroll_x
            if pygame.sprite.collide_rect(player, gem):
                player.is_blocked = True
                isFinish = True
                
                font = pygame.font.Font(None, 72)
                text = font.render(text_time + "    " + str(player.age) + " ans", True, colors.WHITE)
                
                # Obtenir le rectangle du texte rendu pour ses dimensions
                text_rect = text.get_rect()
                
                # Calculer la position centrée
                text_rect.center = (conf_screen.WIDTH_SCREEN // 2 , 618)
                scaled_image = pygame.transform.scale(image, (conf_screen.WIDTH_SCREEN, conf_screen.HEIGHT_SCREEN))
                
                # Afficher l'image adaptée à l'écran
                screen.blit(scaled_image, (0, 0))  # Affiche l'image redimensionnée pour couvrir tout l'écran

                # Dessiner le texte centré à l'écran
                screen.blit(text, text_rect)

        if player.is_dead:
            player.is_blocked = True
            isFinish = True

            font = pygame.font.Font(None, 72)
            text = font.render("You died ! You lost the game", True, colors.RED)
            
            # Obtenir le rectangle du texte rendu pour ses dimensions
            text_rect = text.get_rect()
            
            # Calculer la position centrée
            text_rect.center = (conf_screen.WIDTH_SCREEN // 2 , conf_screen.HEIGHT_SCREEN // 2)

            # Dessiner le texte centré à l'écran
            screen.blit(text, text_rect)

        clock.tick(60)
        pygame.display.flip()

pygame.quit()