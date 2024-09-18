import pygame
import os
import config.screen as conf_screen
import config.colors as colors
import entities.player as player_config
import terrain.Platformer as platformer
import season_cycle as season_cycle_manager

pygame.init()

screen = pygame.display.set_mode((conf_screen.WIDTH_SCREEN, conf_screen.HEIGHT_SCREEN))
grid = [[0 for x in range(conf_screen.COLS)] for y in range(conf_screen.ROWS)]

season_cycle = season_cycle_manager.SeasonCycle(screen, conf_screen.CELL_SIZE*2, conf_screen.CELL_SIZE*2, conf_screen.CELL_SIZE*.2, conf_screen.CELL_SIZE*.2)

pygame.display.set_caption("Seasonal Odyssey")

GRAVITE = 0.8
SCROLL_SPEED = 5  
SCROLL_THRESHOLD = 0.85 * conf_screen.WIDTH_SCREEN 

PATH = os.path.dirname(__file__)

SEASONS = ["Printemps", "Été", "Automne", "Hiver"]
current_season_index = 0
season_change_time = 5000  # 5 secondes en millisecondes
last_season_change = pygame.time.get_ticks()


sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

player = player_config.Player()
sprites.add(player)

platforms_data = [
    (conf_screen.WIDTH_SCREEN, 20, 0, conf_screen.HEIGHT_SCREEN - 100), 
    (200, 20, 400, conf_screen.HEIGHT_SCREEN - 200),  
    (250, 20, 700, conf_screen.HEIGHT_SCREEN - 300),  
    (300, 20, 1100, conf_screen.HEIGHT_SCREEN - 400), 
    (200, 20, 1500, conf_screen.HEIGHT_SCREEN - 250), 
    (300, 20, 1800, conf_screen.HEIGHT_SCREEN - 150), 
    (250, 20, 2100, conf_screen.HEIGHT_SCREEN - 350), 
    (400, 20, 2500, conf_screen.HEIGHT_SCREEN - 100), 
    (250, 20, 3000, conf_screen.HEIGHT_SCREEN - 200), 
    (300, 20, 3400, conf_screen.HEIGHT_SCREEN - 350)  
]

# Créer les plateformes et les ajouter aux groupes
for data in platforms_data:
    platform = platformer.Platform(*data)
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
            elif event.key == pygame.K_RIGHT:
                player.move_right()
            elif event.key == pygame.K_LEFT:
                player.move_left()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player.stop()

    scroll_x = 0
    if player.rect.right > SCROLL_THRESHOLD:
        scroll_x = SCROLL_SPEED

    # Ici on fait défiler toutes les plateformes
    platforms.update(scroll_x)
    if not player.is_grounded:
        player.gravite()

    player.rect.x += player.x_current_speed
    player.rect.y += player.y_current_speed

    # Le joueur ne peut pas sortir de l'écran à gauche (limite de la fenêtre du début)
    if player.rect.left < 0:
        player.rect.left = 0

    # Si le joueur tombe sous l'écran, il meurt et le jeu recommence au TOUT début en remontant meme le background et remettant le joueur en position initiale
    if player.rect.top > conf_screen.HEIGHT_SCREEN:
        player.rect.x = 400
        player.rect.y = conf_screen.HEIGHT_SCREEN - 400
        player.is_grounded = False
        player.y_current_speed = 0
        player.x_current_speed = 0

        
    # Gestion des collisions entre le joueur et les plateformes
    collided_platform = pygame.sprite.spritecollide(player, platforms, False)
    if collided_platform:
        player.is_grounded = True
        player.y_current_speed = 0
        player.rect.bottom = collided_platform[0].rect.top

    elif not collided_platform:
        player.is_grounded = False

    # Vérifier si 5 secondes se sont écoulées pour changer de saison
    current_time = pygame.time.get_ticks()
    if current_time - last_season_change > season_change_time:
        current_season_index = (current_season_index + 1) % len(SEASONS)
        last_season_change = current_time

    screen.fill(colors.WHITE)
    
    conf_screen.draw_grid(grid, screen)

    sprites.draw(screen)
    
    # Mettre à jour et afficher le cycle des saisons
    season_cycle.update_needle_rotation()
    season_cycle.show_season_cycle()

    # Afficher la saison actuelle
    current_season = season_cycle.current_season()
    print(f"Saison actuelle: {current_season}")
    pygame.display.flip()
    
    # print(season_cycle.elapsed_time)
    # print(season_cycle.year_elapsed(season_cycle.elapsed_time))

    season_cycle.elapsed_time = pygame.time.get_ticks() // (1000//8)
    clock.tick(60)

pygame.quit()