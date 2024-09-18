import pygame
import  config.colors as colors

WIDTH_SCREEN = 1280
HEIGHT_SCREEN = 896

CELL_SIZE = 64
ROWS = HEIGHT_SCREEN // CELL_SIZE
COLS = WIDTH_SCREEN // CELL_SIZE

def draw_grid(grid, screen):
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[y][x] == 1:
                pygame.draw.rect(screen, colors.RED, rect)
            else:
                pygame.draw.rect(screen, colors.BLACK, rect, 1)