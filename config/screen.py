import pygame
import config.colors as colors

pygame.init()

COLS = 20
ROWS = 14
PADDING = 50  # 50 pixels de marge de chaque côté

info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

CELL_SIZE = min((screen_width - 2 * PADDING) // COLS, (screen_height - 2 * PADDING) // ROWS)

WIDTH_SCREEN = CELL_SIZE * COLS
HEIGHT_SCREEN = CELL_SIZE * ROWS

def draw_grid(grid, screen):
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, colors.BLACK, rect, 1)
