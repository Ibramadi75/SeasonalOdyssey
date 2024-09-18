import pygame
import config.colors as colors
import config.screen as conf_screen

GRAVITE = .8

PLAYER_IMG = pygame.Surface((50, 50))
PLAYER_IMG.fill(colors.RED)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = conf_screen.HEIGHT_SCREEN - 400
        self.is_grounded = False
        self.x_current_speed = 0
        self.y_current_speed = 0
        self.move_speed = 6
        self.jump_speed = 15
        self.age = 12
        
    def update(self):
        if not self.is_grounded:
            self.gravite()
        
        self.rect.x += self.x_current_speed
        self.rect.y += self.y_current_speed
        
        if self.rect.right >conf_screen.WIDTH_SCREEN:
            self.rect.right = conf_screen.WIDTH_SCREEN
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > conf_screen.HEIGHT_SCREEN:
            self.rect.bottom = conf_screen.HEIGHT_SCREEN
            self.is_grounded = True
            self.y_current_speed = 0

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
        
    def state(self):
        return self.age / 18
    
    def die():
        return;
        
    def grow(self):
        self.age += 1
        
        if (self.state == 1):
            self.image = pygame.Surface((50, 50))
            self.image.fill(colors.YELLOW)
        elif (self.state == 2):
            self.image = pygame.Surface((100, 100))
            self.image.fill(colors.BLUE)
        elif (self.state == 3):
            self.image = pygame.Surface((150, 150))
            self.image.fill(colors.GREEN)
        else: 
            self.die()
            
        
        

        