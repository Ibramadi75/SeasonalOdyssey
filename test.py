import pygame
import pytmx
import time

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
screen_width = 1600
screen_height = 1200
screen = pygame.display.set_mode((screen_width, screen_height))

# Titre de la fenêtre
pygame.display.set_caption("Changement de layers par saison")

# Chargement de la carte .tmx
tmx_data = pytmx.util_pygame.load_pygame('map.tmx')

# Facteur de scaling
SCALE_FACTOR = 2

# Définitions des saisons et layers associés
seasons = ["printemps", "automne"] #["printemps", "été", "automne", "hiver"]
season_layers = {
    "printemps": ["spring_layer"],
    # "été": ["summer_layer"],
    "automne": ["autumn_layer"],
    # "hiver": ["winter_layer"]
}

collision_rects = []

# On parcourt tous les objets du layer de collision (nommé "collision_layer" dans Tiled)
for layer in tmx_data.visible_layers:
    if isinstance(layer, pytmx.TiledObjectGroup):
        if layer.name == "collision_layer":
            for obj in layer:
                # Crée un rectangle pour chaque objet de collision
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                collision_rects.append(rect)

print(collision_rects)

# Fonction pour dessiner les layers spécifiés et appliquer le scaling
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

# Variables pour gérer le changement de saison
current_season_index = 0
current_season = seasons[current_season_index]
last_change_time = time.time()

# Boucle principale du jeu
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Vérifie si 5 secondes se sont écoulées pour changer de saison
    current_time = time.time()
    if current_time - last_change_time >= 5:
        # Change de saison
        current_season_index = (current_season_index + 1) % len(seasons)
        current_season = seasons[current_season_index]
        
        # Met à jour le temps du dernier changement
        last_change_time = current_time

    # Remplir l'écran avec une couleur noire
    screen.fill((0, 0, 0))

    # Dessiner les layers correspondant à la saison courante
    draw_specific_layers(season_layers[current_season])

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter le FPS pour éviter de surcharger le CPU
    pygame.time.Clock().tick(60)

# Quitter Pygame
pygame.quit()
