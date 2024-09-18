import pygame
import config.colors as colors

NUMBER_OF_SEASONS = 4
TOTAL_TIME_PER_YEAR = 360
SEASON_DURATION = TOTAL_TIME_PER_YEAR // NUMBER_OF_SEASONS

NEEDLE_WIDTH = 6
NEEDLE_HEIGHT = 50

NEEDLE_IMAGE_PATH = "assets/clock_needle.png"

SEASONS = ["Spring", "Summer", "Autumn", "Winter"]

def show_season_cycle(screen, width, height, x, y, rotation_angle = 0):
    image = pygame.image.load("assets/FourSeasonsSymbolic.png")
    resized_image = pygame.transform.scale(image, (width, height))
    
    center_x = x + width // 2
    center_y = y + height // 2
    
    rotated_image = pygame.transform.rotate(resized_image, rotation_angle)
    rotated_rect = rotated_image.get_rect(center=(center_x, center_y))
    
    screen.blit(rotated_image, rotated_rect.topleft)
    
    draw_needle(screen, center_x, center_y - height // 5)
    
def time_to_angle(time):
    return time


def draw_needle(screen, center_x, center_y, rotation_angle=0):
    needle = pygame.Surface((NEEDLE_WIDTH, NEEDLE_HEIGHT), pygame.SRCALPHA)
    needle.fill((0, 0, 0, 0))
    pygame.draw.rect(needle, colors.BLACK, pygame.Rect(0, 0, NEEDLE_WIDTH, NEEDLE_HEIGHT))
    
    if rotation_angle != 0:
        needle = pygame.transform.rotate(needle, rotation_angle)
    
    needle_rect = needle.get_rect(center=(center_x, center_y))
    screen.blit(needle, needle_rect.topleft)
    
def current_season(elapsed_time):
    current_season_index = (elapsed_time // SEASON_DURATION) % NUMBER_OF_SEASONS
    return SEASONS[current_season_index]
