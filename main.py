import pygame
import os
import config.screen as conf_screen
import config.colors as colors
import entities.player as player_config
import terrain.Platformer as platformer
import season_cycle as season_cycle_manager
import pytmx

# os.environ['SDL_VIDEO_WINDOW_POS'] = f"{conf_screen.PADDING},{conf_screen.PADDING}"
pygame.mixer.init()

# Load the music file
music_path = 'music/sound_theme2.mp3'
if os.path.exists(music_path):
    print("Music file found!")
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
SCROLL_SPEED = 1.5  
SCROLL_THRESHOLD = 0.35 * conf_screen.WIDTH_SCREEN 

PATH = os.path.dirname(__file__)


# Charger l'image
background_image = pygame.image.load('assets/winter/background/background.png').convert()
background_image = pygame.transform.scale(background_image, (conf_screen.WIDTH_SCREEN, conf_screen.HEIGHT_SCREEN))

SEASONS = ["Printemps", "Été", "Automne", "Hiver"]
current_season_index = 0
season_change_time = 5000  # 5 secondes en millisecondes
last_season_change = pygame.time.get_ticks()

sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

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

scroll_x_camera = 0
scroll_x = 0

clock = pygame.time.Clock()
isRunning = True

while isRunning:
    scroll_x = 0
    actual_platforms = remove_all_but_one_group(platforms, "terrain")
    sprites = remove_all_but_one_group(sprites, "terrain")

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

    scroll_x_camera += player.x_current_speed * SCROLL_SPEED if player.rect.right > SCROLL_THRESHOLD else 0
                
    if player.rect.right > SCROLL_THRESHOLD:
        scroll_x = player.x_current_speed * SCROLL_SPEED

    # Ici on fait défiler toutes les plateformes
    platforms.update(scroll_x)

    # Le joueur ne peut pas sortir de l'écran à gauche (limite de la fenêtre du début)
    if player.rect.left < 0:
        player.rect.left = 0

    # Si le joueur tombe sous l'écran, il meurt et le jeu recommence au TOUT début en remontant meme le background et remettant le joueur en position initiale
    if player.rect.top > conf_screen.HEIGHT_SCREEN:
        print('out')
        player.rect.x = 400
        player.rect.y = conf_screen.HEIGHT_SCREEN - 400
        player.is_grounded = False
        player.y_current_speed = 0
        player.x_current_speed = 0

    # Gestion des collisions entre le joueur et les plateformes
    

    # Vérifier si 5 secondes se sont écoulées pour changer de saison
    current_time = pygame.time.get_ticks()
    if current_time - last_season_change > season_change_time:
        current_season_index = (current_season_index + 1) % len(SEASONS)
        last_season_change = current_time

    screen.blit(background_image, (0, 0))
    
    #conf_screen.draw_grid(grid, screen)

    sprites.draw(screen)
    
    # Mettre à jour et afficher le cycle des saisons
    season_cycle.update_needle_rotation()
    season_cycle.show_season_cycle()
    
    player.update_age(season_cycle.year_elapsed())

    # Afficher la saison actuelle
    current_season = season_cycle.current_season()

    # Afficher les layers de la saison actuelle avec le défilement
    current_season = season_cycle.current_season()
    draw_visible_tiles(season_cycle.SEASON_LAYERS['Spring'], scroll_x_camera)

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

    # if current_season in ['Spring', 'Autumn']:
    #     draw_specific_layers(season_cycle.SEASON_LAYERS[current_season], scroll_x, player.rect.x)
    player.show_age(screen)
    player.is_jumping = False

    player.update(actual_platforms)
    # actual_platforms.draw(screen)

    collided_platform = pygame.sprite.spritecollide(player, actual_platforms, False)
    if collided_platform:
        player.is_grounded = True
        player.y_current_speed = 0
        player.rect.bottom = collided_platform[0].rect.top

    elif not collided_platform:
        player.is_grounded = False

    pygame.display.flip()

    if (player.state == 2):
        season_cycle.elapsed_time = pygame.time.get_ticks() // (1000//64)
    else:
        season_cycle.elapsed_time = pygame.time.get_ticks() // (1000//32)
    clock.tick(60)

pygame.quit()