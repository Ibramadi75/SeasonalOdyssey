import pygame
import config.colors as colors

pygame.init()

# On maintient 20 colonnes et 14 rangées
COLS = 36
ROWS = 24
PADDING = 500  # 50 pixels de marge de chaque côté

info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

CELL_SIZE = min((screen_width - 2 * PADDING) // COLS, (screen_height - 2 * PADDING) // ROWS)

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
