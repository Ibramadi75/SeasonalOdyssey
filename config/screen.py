import pygame
import config.colors as colors

# Initialiser Pygame avant d'utiliser display.Info()
pygame.init()

# On maintient 20 colonnes et 14 rangées
COLS = 36
ROWS = 24

# Récupérer les informations de l'écran
info = pygame.display.Info()

# Calculer la taille de l'écran en fonction de la taille des cellules
WIDTH_SCREEN = info.current_w
HEIGHT_SCREEN = info.current_h

# Calculer la taille des cellules en fonction de la résolution actuelle de l'écran
CELL_SIZE = 32

# Redéfinir les dimensions de l'écran pour s'adapter exactement à 14x20 cellules
WIDTH_SCREEN = CELL_SIZE * COLS
HEIGHT_SCREEN = CELL_SIZE * ROWS

def draw_grid(grid, screen):
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, colors.BLACK, rect, 1)
