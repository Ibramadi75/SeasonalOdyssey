import pygame
import config.colors as colors
import config.screen as screen

GRAVITE = .8

PLAYER_IMG = pygame.Surface((50, 50))
PLAYER_IMG.fill(colors.RED)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = screen.HEIGHT_SCREEN - 400
        self.is_grounded = False
        self.x_current_speed = 0
        self.y_current_speed = 0
        self.move_speed = 10
        self.jump_speed = 10

    def gravite(self):
        if not self.is_grounded:
            self.y_current_speed += GRAVITE

    def jump(self):
        if self.is_grounded:
            self.y_current_speed = -self.jump_speed
            self.is_grounded = False

    def move_right(self):
        self.x_current_speed = self.move_speed

    def move_left(self):
        self.x_current_speed = -self.move_speed

    def stop(self):
        self.x_current_speed = 0