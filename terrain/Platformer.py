import pygame
import config.colors as colors

class Platform(pygame.sprite.Sprite):
    def __init__(self, largeur, hauteur, x, y):
        super().__init__()
        self.image = pygame.Surface((largeur, hauteur))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll_x):
        """Fait défiler la plateforme en fonction du déplacement du joueur."""
        self.rect.x -= scroll_x

        
    