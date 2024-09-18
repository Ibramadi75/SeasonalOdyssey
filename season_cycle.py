import pygame
import config.colors as colors

class SeasonCycle:
    NUMBER_OF_SEASONS = 4
    TOTAL_TIME_PER_YEAR = 360
    SEASON_DURATION = TOTAL_TIME_PER_YEAR // NUMBER_OF_SEASONS

    NEEDLE_WIDTH = 6
    NEEDLE_HEIGHT = 50
    NEEDLE_IMAGE_PATH = "assets/clock_needle.png"

    SEASONS = ["Spring", "Summer", "Autumn", "Winter"]
    SEASON_LAYERS = {
        "Spring": ["spring_layer"],
        # "Summer": ["summer_layer"],
        "Autumn": ["autumn_layer"],
        # "Winter": ["winter_layer"]
    }

    def __init__(self, screen, width, height, x, y):
        self.screen = screen
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.rotation_angle = 0 
        self.center_x = x + width // 2
        self.center_y = y + height // 2
        
        self.elapsed_time = 0

        self.image = pygame.image.load("assets/FourSeasonsSymbolic.png")
        self.resized_image = pygame.transform.scale(self.image, (self.width, self.height))

    def show_season_cycle(self):
        rotated_image = pygame.transform.rotate(self.resized_image, self.rotation_angle)
        rotated_rect = rotated_image.get_rect(center=(self.center_x, self.center_y))
        self.screen.blit(rotated_image, rotated_rect.topleft)
        
        self.draw_needle(self.center_x, self.center_y - self.height // 5)

    def time_to_angle(self, elapsed_time):
        return (elapsed_time % SeasonCycle.TOTAL_TIME_PER_YEAR) / SeasonCycle.TOTAL_TIME_PER_YEAR * 360

    def draw_needle(self, center_x, center_y, rotation_angle=0):
        needle = pygame.Surface((SeasonCycle.NEEDLE_WIDTH, SeasonCycle.NEEDLE_HEIGHT), pygame.SRCALPHA)
        needle.fill((0, 0, 0, 0))
        pygame.draw.rect(needle, colors.BLACK, pygame.Rect(0, 0, SeasonCycle.NEEDLE_WIDTH, SeasonCycle.NEEDLE_HEIGHT))

        if rotation_angle != 0:
            needle = pygame.transform.rotate(needle, rotation_angle)

        needle_rect = needle.get_rect(center=(center_x, center_y))
        self.screen.blit(needle, needle_rect.topleft)

    def update_needle_rotation(self):
        self.rotation_angle = self.time_to_angle(self.elapsed_time)

    def current_season(self):
        current_season_index = (self.elapsed_time // SeasonCycle.SEASON_DURATION) % SeasonCycle.NUMBER_OF_SEASONS
        return SeasonCycle.SEASONS[current_season_index]

    def year_elapsed(self, elapsed_time):
        return (elapsed_time // SeasonCycle.TOTAL_TIME_PER_YEAR)
